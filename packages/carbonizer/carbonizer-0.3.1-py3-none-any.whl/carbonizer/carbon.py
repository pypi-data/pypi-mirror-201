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


@dataclasses.dataclass
class Carbonizer:
    input_file: pathlib.Path
    output_file: pathlib.Path
    exclude: str
    background: utils.RGBA = utils.RGBA(0, 0, 0, 0)
    font: str = "Night Owl"

    async def __call__(self):
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
        # TODO: refactor to make this SRP compatible

        data = {"code": quote(code.encode("utf-8")),
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "shadow": True,
                "theme": self.font
                }
        validated_body = utils.validate_body(data)
        carbon_url = utils.create_url(validated_body)
        with tempfile.TemporaryDirectory() as tmp_path:
            await (self.get_response(carbon_url, tmp_path))
            expected_file = pathlib.Path(tmp_path) / "carbon.png"
            if expected_file.exists():
                shutil.move(expected_file, self.output_file.absolute())
                # ERROR: this can cause errors as temfiles seems to be on a different mounts on LINUX
                # expected_file.rename(self.output_file.absolute())
            else:
                # TODO: create proper Exception to reflect error
                raise Exception(f"Couldnt download carbonized version of {self.input_file}")

        return self.output_file

    async def get_response(self, url, tmp_path):
        # TODO: test if this works for all cenarios
        # TODO remove comments
        browser, page = await open_carbonnowsh(url, tmp_path)  # FIXME - let python create a temporary path
        # element = await page.querySelector("#export-container  .container-bg")
        # element = await page.querySelector(".react-codemirror2")
        # await element.screenshot({'path': self.output_filename.absolute()})
        el = await page.querySelector(".CodeMirror > div:nth-child(1) > textarea:nth-child(1)")
        await el.type(" ") # Force editor to adjust layout
        el = await page.querySelector(".jsx-2184717013")
        await el.click()
        # TODO: find better way to wait for carbon file
        # TODO: likely watch for file instead of fixed timeout
        await page.waitFor(2000)
        await browser.close()

    def is_valid(self) -> bool:
        res = False
        if self.input_file.is_file():
            res = True
        if re.search(self.exclude, self.input_file.absolute().__str__()):
            logger.debug(f"Skipping file - {self.input_file}")
            res = False
        return res


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
