import dataclasses
import asyncio
import pathlib
import re
import tempfile
import shutil
from urllib.parse import quote

from loguru import logger
from pyppeteer import launch

from carbonizer import utils


class CarbonNowException(Exception):
    ...


@dataclasses.dataclass
class Carbonizer:
    input_file: pathlib.Path
    output_file: pathlib.Path
    exclude: str
    background: utils.RGBA = utils.RGBA(0, 0, 0, 0)
    font: str = "Night Owl"
    temp_carbon: str = "carbon.png"
    file_beat: int = 500
    limit: int = 5000

    async def __call__(self):
        await  self.run_async()

    def run(self):
        asyncio.run(self.run_async())

    async def run_async(self):
        if not self.is_valid():
            return False
        try:
            with open(self.input_file, "r") as f:
                code = f.read()
            await self.carbonize_code(code)
        except Exception as e:
            logger.error(f"Failed to carbonize {self.input_file} - due to: {e}")
            return False
        else:
            return True

    async def carbonize_code(self, code):
        data = {"code": quote(code.encode("utf-8")),
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "shadow": True,
                "theme": self.font
                }
        validated_body = utils.validate_body(data)
        carbon_url = utils.create_url(validated_body)
        with tempfile.TemporaryDirectory() as tmp_path:
            expected_file = await (self.get_response(carbon_url, tmp_path))
            shutil.move(expected_file, self.output_file.absolute())
        return self.output_file

    async def get_response(self, url, tmp_path):
        expected_file = pathlib.Path(tmp_path) / self.temp_carbon
        browser, page = await open_carbonnowsh(url, tmp_path)
        el = await page.querySelector(".CodeMirror > div:nth-child(1) > textarea:nth-child(1)")
        await el.type(" ") # Force editor to adjust layout
        el = await page.querySelector(".jsx-2184717013")
        await el.click()
        success = await self.check_file_exists(expected_file)
        await browser.close()
        if not success:
            raise CarbonNowException(f"Could not download file in time - try again and maybe increase the limit ")
        return expected_file

    def is_valid(self) -> bool:
        res = False
        if self.input_file.is_file():
            res = True
        if re.search(self.exclude, self.input_file.absolute().__str__()):
            logger.debug(f"Skipping file - {self.input_file}")
            res = False
        return res

    async def check_file_exists(self,file: pathlib.Path) -> bool:
        counter = 0
        while True:
            if file.exists():
                return True
            elif counter >= self.limit:
                return False
            else:
                counter += self.file_beat
                await asyncio.sleep(self.file_beat)


async def open_carbonnowsh(url, tmp_path):
    browser = await launch(
        defaultViewPort=None,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page._client.send('Page.setDownloadBehavior', {
        'behavior': 'allow',
        'downloadPath': tmp_path
    })
    await page.goto(url, timeout=100000)
    return browser, page
