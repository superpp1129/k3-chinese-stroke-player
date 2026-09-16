"""Native Chromium UI/media acceptance; no browser profile or credentials."""
import json,os,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8877/'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path=os.environ.get('BROWSER_EXECUTABLE'))
    page=browser.new_page(viewport={'width':1280,'height':1000});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url);page.wait_for_load_state('networkidle')
    assert page.locator('.character-card').count()==21
    assert page.locator('.word-card').count()==8
    page.screenshot(path=str(ROOT/'verification/ui-desktop.png'),full_page=True)
    checks=[]
    buttons=page.locator('[data-video]')
    for i in range(buttons.count()):
        button=buttons.nth(i);char=button.get_attribute('data-char');src=button.get_attribute('data-video')
        button.click();page.wait_for_function("document.querySelector('video').readyState>=2")
        details=page.locator('video').evaluate('(v)=>({src:v.getAttribute("src"),width:v.videoWidth,height:v.videoHeight,duration:v.duration,paused:v.paused})')
        assert details['src']==src and details['width']==1080 and details['height']==1080,(char,details)
        page.wait_for_function("document.querySelector('video').currentTime>0")
        page.locator('#replay').click()
        assert page.locator('#dialog-download').get_attribute('download')==f'{char}字彩色筆順動畫.mp4'
        page.keyboard.press('Escape');page.wait_for_function("!document.querySelector('dialog').open && document.querySelector('video').paused")
        checks.append({'char':char,'src':src,**details})
    for a in page.locator('.character-card .download').all():
        response=page.request.get(url+a.get_attribute('href'))
        assert response.status==200
        assert len(response.body())>1000
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(ROOT/'verification/ui-phone.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('[aria-label="播放「防」字筆順"]').click();page.wait_for_function("document.querySelector('video').readyState>=2")
    page.screenshot(path=str(ROOT/'verification/ui-player-phone.png'))
    assert not errors,errors
    report={'url':url,'buttons_exercised':len(checks),'character_cards':21,'word_cards':8,'downloads':21,'native_playback_checks':checks,'page_errors':errors,'phone_width':390,'horizontal_overflow':False}
    (ROOT/'verification'/('ui-live.json' if 'github.io' in url else 'ui-local.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({'url':url,'buttons':len(checks),'downloads':21,'errors':errors},ensure_ascii=False))
    browser.close()
