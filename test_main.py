"""
test_main.py: šestý projekt do Engeto Online Python Akademie

author: David Horák
email: daviiid739@gmail.com
"""
from playwright.sync_api import Page, expect

ENGETO_URL = "https://engeto.cz/"
TERMINY_KURZU_URL = "https://engeto.cz/terminy/"

# --- HELPER FUNKCE ---
def reject_cookies(page: Page):
    """Pomocná funkce pro zavření cookies overlaye"""  
    btn = page.locator("#cookiescript_reject")
    if btn.is_visible():
        btn.click()

# --- TESTY ---
def test_goto_terminy_kurzu(page: Page):
    """
    Ověří že hover na 'Kurzy' v hlavním menu zobrazí dropdown 
    a klik na 'Zobrazit termíny kurzů' přesměruje na stránku termínů.
    """
    page.goto(ENGETO_URL)

    reject_cookies(page)

    # rozbal dropdown "Kurzy"
    kurzy_btn = page.locator("#top-menu").get_by_role("link", name="Kurzy")
    kurzy_btn.hover()

    # kliknutí na tlačítko "Zobrazit termíny kurzů"
    terminy_kurzu_btn = page.get_by_role("link", name="Zobrazit termíny kurzů")
    terminy_kurzu_btn.click()

    # kontrola nové url
    expect(page).to_have_url("https://engeto.cz/terminy/")


def test_filtr_terminy_kurzu(page: Page):
    """
    Ověří že filtrování na stránce termínů funguje správně —
    po zaškrtnutí filtrů 'Python' a 'Akademie (1,5–3 měsíce)' 
    jsou zobrazeny pouze kurzy 'Python Akademie'.
    """
    page.goto(TERMINY_KURZU_URL)

    reject_cookies(page)

    # zaškrtnout checkboxy
    python_checkbox = page.get_by_role("checkbox", name="Python")
    python_checkbox.check()

    akademie_checkbox = page.get_by_role("checkbox", name="Akademie (1,5–3 měsíce)")
    akademie_checkbox.check()

    # Playwright umí filtrovat přímo na locatoru
    python_akademie_h3 = page.get_by_role("heading", name="Python Akademie", level=3)

    # ověř že všechny nalezené h3 jsou viditelné a obsahují text "Python Akademie"
    for h3 in python_akademie_h3.all():
        expect(h3).to_be_visible()
        expect(h3).to_have_text("Python Akademie")


def test_pridat_kurz_do_kosiku(page: Page):
    """
    Ověří celý flow přidání kurzu do košíku — od homepage přes detail kurzu
    a výběr termínu až po ověření obsahu košíku s správným množstvím.
    """
    page.goto(ENGETO_URL)

    reject_cookies(page)

    # kliknout na tlačítko "Více informací" na kartě "Datový analytik s Pythonem"
    page.locator(".card", has_text="Datový analytik s Pythonem").get_by_text("Více informací").click()

    # kliknout na tlačítko "Zobrazit termíny kurzu"
    page.locator("a[href='#terminy']", has_text="Zobrazit termíny kurzu").click()

    # kliknout na první kartu "Datový analytik s Pythonem"
    page.locator(".dates-filter-product[href*='datovy-analytik-s-pythonem']").first.click()

    # kliknout na tlačítko "Objednat kurz"
    page.locator("a[href*='add-to-cart']").click()

    # očekávej produkt v košíku
    expect(page.locator(".cart_item").get_by_role("link", name="Datový analytik s Pythonem")).to_be_visible()

    # očekávej množství 1
    expect(page.locator(".cart_item").get_by_label("Množství")).to_have_value("1")
    
