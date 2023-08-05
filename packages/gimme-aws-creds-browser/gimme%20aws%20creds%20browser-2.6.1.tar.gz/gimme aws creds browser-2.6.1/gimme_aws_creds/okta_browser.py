from playwright.sync_api import Playwright, sync_playwright, expect
from .ui import CLIUserInterface

class OktaBrowser(object):

  def __init__(self, ui: CLIUserInterface ):
    self.ui = ui

  def get_saml_response(self, url, email, password):
    """Get SAML response from Okta using Playwright."""
    if not email or not password:
      raise ValueError("Email or password is empty")

    with sync_playwright() as playwright:
      browser = playwright.chromium.launch(headless=True, slow_mo=250)
      context = browser.new_context()
      page = context.new_page()
      self.ui.info("Opening Okta login page. It will auto populate your credentials and click to send push notification.")
      page.goto(url)
      page.get_by_role("textbox", name="Email").click()
      page.get_by_role("textbox", name="Email").fill(email)
      page.get_by_role("button", name="Next").click()
      page.get_by_role("textbox", name="Password").click()
      page.get_by_role("textbox", name="Password").fill(password)
      page.get_by_role("button", name="Verify").click()
      page.get_by_role("link", name="Select").nth(1).click()

      self.ui.notify("You will shortly receive a push notification on your phone. Please approve it.")
      
      page.get_by_text("Select a role:").select_text()
      expect(page).to_have_title("Amazon Web Services Sign-In")

      saml_response = page.get_attribute("input[name=SAMLResponse]", "value")
      target_url = page.url
      
      context.close()
      browser.close()

      return {'SAMLResponse': saml_response, 'RelayState': None, 'TargetUrl': target_url}
