import asyncio
import pyppeteer
from PIL import Image
from pyppeteer import launch
from pyppeteer.launcher import Launcher
from pyppeteer.dialog import Dialog
from .tools import retry
from .constants import PROXY_USER, PROXY_PASSWORD
from .base import Config
from .data_analisys import PV


DEBUG = True
PROXY = ''


class Jml(Config, PV):

    ARGS = ['--no-sandbox', '--disable-infobars', f'--window-size=1024,768', f'--proxy-server={PROXY}']
    HEADLESS = False if DEBUG else True
    VIEW_WIDTH = 1024
    VIEW_HEIGHT = 768
    LOGIN = False
    LOGIN_URL = 'https://jmlnt.forest.gov.tw/index.php'
    ROOM_URL = 'https://jmlnt.forest.gov.tw/room/order_terms.php?date={date}'.format
    MEMBERS_URL = 'https://jmlnt.forest.gov.tw/room/index.php?member_num={members}'.format

    async def start(self):
        """登入"""
        browser = await self._launch()
        try:
            page = await self._start_page(browser)
            await self.config_proxy(page)
            await self._start(page)
            await asyncio.sleep(2)
        except Exception as e:
            print(e)
            raise e
        finally:
            await browser.close()
        return '程序完成'

    @retry
    async def _start(self, page):
        """"""
        if not self.LOGIN:
            await self.login(page)
        await self.operate(page, datetime_='2022-07-22')

    async def login(self, page):
        """登入"""
        await page.goto(self.LOGIN_URL)
        await asyncio.sleep(2)
        # 帳號區塊處理(選取、輸入)
        account_x = '//*[@id="is_uu"]'
        await page.waitForXPath(account_x)
        username = await page.xpath(account_x)
        await username[0].type('kevin61517')
        await asyncio.sleep(2)
        # 密碼區塊處理(選取、輸入)
        pw_x = '//*[@id="is_pp"]'
        await page.waitForXPath(pw_x)
        password = await page.xpath(pw_x)
        await password[0].type('61517kevin')
        await asyncio.sleep(0.5)
        # 準備點擊登入按鈕
        login_x = '//*[@id="login-form-submit"]'
        await page.waitForXPath(login_x)
        login = await page.xpath(login_x)
        await login[0].click()
        await asyncio.sleep(5)

    async def operate(self, page, datetime_=None):
        """操作"""
        if int(self.team_data["members"]) != len(self.member_data):
            raise ValueError('會員資料數目與人數不符!')
        await self._choose_date(page, datetime_=datetime_)
        await self._roll_down(page)
        await self._agree(page)
        await self._set_team(page)
        await self._set_member(page)
        await self._set_beds(page)
        input('按任意鍵繼續')
        # await self._picture_valid(page)
        # await self._set_payment(page)
        # await asyncio.sleep(10)

    async def _choose_date(self, page, datetime_):
        """選擇日期"""
        await asyncio.sleep(2)
        await page.goto(self.ROOM_URL(date=datetime_))
        await asyncio.sleep(3)

    @staticmethod
    async def _roll_down(page):
        """滾動頁面"""
        await page.evaluate("""{window.scrollBy(0, document.body.scrollHeight);}""")
        await asyncio.sleep(2)

    @staticmethod
    async def _agree(page):
        """點擊同意"""
        agree_x = '//*[@id="agree"]'
        await page.waitForXPath(agree_x)
        agree = await page.xpath(agree_x)
        await agree[0].click()
        await asyncio.sleep(2)

    async def _set_team(self, page):
        """隊伍相關設置：名稱、計畫、無線電"""
        # 隊伍名稱
        name_x = '//*[@id="team_name"]'
        await page.waitForXPath(name_x)
        name = await page.xpath(name_x)
        await name[0].type(self.team_data['name'])
        await asyncio.sleep(1)
        # 隊伍計畫
        schedule_x = '//*[@id="schedule"]'
        await page.waitForXPath(schedule_x)
        schedule = await page.xpath(schedule_x)
        await schedule[0].type(self.team_data['schedule'])
        await asyncio.sleep(1)
        # 無線電
        radio_x = '//*[@id="radio"]'
        await page.waitForXPath(radio_x)
        radio = await page.xpath(radio_x)
        await radio[0].type(self.team_data['radio'])
        await asyncio.sleep(3)

    async def _set_member(self, page):
        """
        隊員相關設置：人數、個資
        Example: <select>
                    <option value="10">10</option>
                </select>
        填入 10 即可
        """
        members = int(self.team_data["members"])
        # 選擇隊員人數
        members_s = '#main > table:nth-child(5) > tbody > tr:nth-child(2) > th > select'
        await page.waitForSelector(members_s)
        await page.select(members_s, f'{members}')
        await asyncio.sleep(5)
        # 隊員資料
        no = 0
        while no < members:
            if no == 0:
                await self._member_emergency(page, no)
            else:
                await self._member_detail(page, no)
                await self._member_emergency(page, no)
            no += 1
        await asyncio.sleep(2)

    async def _member_detail(self, page, no):
        """"""
        # 隊員名字
        name_x = '//*[@id="team_detail[1][name]"]'
        await page.waitForXPath(name_x)
        name = await page.xpath(name_x)
        await name[0].type(self.member_data[no]['name'])
        await asyncio.sleep(2)
        # 隊員身分證
        id_x = '//*[@id="team_detail[1][idnumber]"]'
        await page.waitForXPath(id_x)
        id_ = await page.xpath(id_x)
        await id_[0].type(self.member_data[no]['id'])
        await asyncio.sleep(2)
        # 隊員生日
        birth_x = '//*[@id="team_detail[1][birth]"]'
        await page.waitForXPath(birth_x)
        birth = await page.xpath(birth_x)
        await birth[0].type(self.member_data[no]['birth'])
        await asyncio.sleep(2)

    async def _member_emergency(self, page, no):
        """"""
        # 緊急聯絡人姓名
        emergency_name_x = f'//*[@id="team_detail[{no}][e_name]"]'
        await page.waitForXPath(emergency_name_x)
        name = await page.xpath(emergency_name_x)
        await name[0].type(self.member_data[no]['emergency_name'])
        await asyncio.sleep(2)
        # 緊急聯絡人電話
        emergency_tel_x = f'//*[@id="team_detail[{no}][e_tel]"]'
        await page.waitForXPath(emergency_tel_x)
        tel = await page.xpath(emergency_tel_x)
        await tel[0].type(self.member_data[no]['emergency_tel'])
        await asyncio.sleep(2)

    async def _set_beds(self, page):
        """選擇床數"""
        bed_s = '#main > table:nth-child(9) > tbody > tr:nth-child(6) > td:nth-child(5) > select'
        await page.waitForSelector(bed_s)
        await page.select(bed_s, f'{self.team_data["members"]}')
        await asyncio.sleep(5)

    @staticmethod
    async def _set_payment(page):
        """設置支付方式與發票"""
        pay_x = '//*[@id="lnvoice_DonateMark"]'
        TRANSFER = 0
        CREDIT_CARD = 1
        E_BILL = 2  # 電子發票
        DONATE_BILL = 3  # 捐贈
        NORMAL_BILL = 4  # 紙本發票
        await page.waitForXPath(pay_x)
        payment = await page.xpath(pay_x)
        await payment[CREDIT_CARD].click()
        await payment[E_BILL].click()

    async def _picture_valid(self, page):
        """圖形驗證"""
        print('開始測試圖形驗證')
        # 擷取驗證碼
        picture_x = '//*[@id="main"]/table[6]/tbody/tr[6]/td/font/div/img'
        picture_x = '//*[@id="main"]/table[6]/tbody/tr[7]/td/font/div/img'
        await page.waitForXPath(picture_x)
        picture = await page.xpath(picture_x)
        print('picture===>', picture)
        await picture[0].screenshot({'path': 'captcha.png'})
        cap = self.analysis('captcha.png')
        await asyncio.sleep(2)

        # 輸入驗證碼
        print('開始輸入驗證碼')
        pv_x = '//*[@id="main"]/table[6]/tbody/tr[7]/td/font/div/input'
        await page.waitFor(pv_x)
        pv = await page.xpath(pv_x)
        await pv[0].type(cap)
        print('驗證碼輸入完成')
        # 點擊確認
        print('點擊確認')
        # check_x = '//*[@id="main"]/table[6]/tbody/tr[7]/td/font/input'
        # await page.waitForXPath(check_x)
        # check = await page.xpath(check_x)
        # await check[0].click()
        await asyncio.sleep(5)

    async def _submit(self, page):
        """"""

    async def _launch(self):
        """获取browser对象"""
        return await launch(headless=self.HEADLESS, args=self.ARGS)

    async def _start_page(self, browser: Launcher):
        """設置瀏覽器頁面"""
        page = await browser.newPage()
        await page.setViewport(viewport={'width': self.VIEW_WIDTH, 'height': self.VIEW_HEIGHT})
        # page.on("dialog", lambda dialog_handle: asyncio.ensure_future(self._handle_dialog(dialog_handle)))
        return page

    @staticmethod
    async def _handle_dialog(dialog: Dialog):
        """禁用談話視窗"""
        await dialog.dismiss()

    @staticmethod
    async def config_proxy(page):
        await page.authenticate({'username': PROXY_USER, 'password': PROXY_PASSWORD})

    def get_binary_img(
            self,
            filename: str,
            binary_value: int = 150,
            is_crop: bool = False,
            crop_size: tuple = None
    ) -> Image.Image:
        """
        :param filename: 文件名
        :param binary_value: 样本集训练得到的值
        :param is_crop:
        :param crop_size:
        :return:
        """
        image = Image.open(filename)
        gray_image = Image.new('L', image.size)
        raw_data = image.getdata()
        gray_data = []
        for rgb in raw_data:
            # value = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
            value = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
            print(rgb, value)
            gray_data.append(0) if value < binary_value else gray_data.append(255)
        gray_image.putdata(gray_data)
        gray_image.save('new.png')
        image.close()
        if is_crop:
            return self.crop(gray_image, crop_size)
        return gray_image

    @staticmethod
    def crop(image: Image, crop_size: tuple) -> Image.Image:
        """
        裁剪
        :param image:
        :param crop_size:
        :return:
        """
        cropped = image.crop(crop_size)
        cropped.save(".png")
        return cropped

    def analysis(self, filename, binary_value=100) -> str:
        """
        :param filename:
        :param binary_value:
        :return:
        """
        crop_size = (2, 2, 115, 31)
        crop_size = (8, 6, 93, 45)
        image = self.get_binary_img(filename, binary_value=binary_value, crop_size=crop_size)
        seg_images = self.split_image(image)
        res = ''
        trained_data = self.get_trained_data(platform='jml')
        for seg_image in seg_images:
            res += self._analysis(seg_image, trained_data)
            seg_image.close()
        image.close()
        return res
