import itertools

from yarl import URL

from ..base_functions.base_functions import get_filename_and_ext, log, logger, make_title_safe
from ..base_functions.data_classes import MediaItem, DomainItem
from ..base_functions.error_classes import NoExtensionFailure
from ..base_functions.sql_helper import SQLHelper
from ..client.client import ScrapeSession


class NSFWXXXCrawler:
    def __init__(self, quiet: bool, separate_posts: bool, SQL_Helper: SQLHelper):
        self.quiet = quiet
        self.separate_posts = separate_posts
        self.SQL_Helper = SQL_Helper

    async def fetch(self, session: ScrapeSession, url: URL) -> DomainItem:
        """Director for NSFW.XXX scraping"""
        domain_obj = DomainItem("nsfw.xxx", {})

        await log(f"Starting: {str(url)}", quiet=self.quiet, style="green")
        if "user" in url.parts:
            await self.get_user(session, url, domain_obj)
        else:
            await self.get_post(session, url, domain_obj)
        await self.SQL_Helper.insert_domain("nsfw.xxx", url, domain_obj)
        return domain_obj

    async def get_user(self, session: ScrapeSession, url: URL, domain_obj: DomainItem):
        """Gets posts for a user profile"""
        try:
            model = url.name + " (NSFW.XXX)"
            for page in itertools.count(1):
                page_url = URL(f"https://nsfw.xxx/page/{page}?nsfw[]=0&types[]=image&types[]=video&types[]=gallery&slider=1&jsload=1&user={url.name}")
                page_soup = await session.get_BS4(page_url)

                posts = page_soup.select('div[class="sh-section__image grid-item"] a[class=slider_init_href]')
                posts.extend(page_soup.select('div[class="sh-video__player"] a[class=slider_init_href]'))
                posts.extend(page_soup.select('div[class="sh-section__images row"] div a'))

                if not posts:
                    break

                posts = await self.get_post_hrefs(posts)
                for post in posts:
                    await self.get_post(session, post, domain_obj, model)

        except Exception as e:
            logger.debug("Error encountered while handling %s", str(url), exc_info=True)
            await log(f"Error: {str(url)}", quiet=self.quiet, style="red")
            logger.debug(e)

    async def get_post_hrefs(self, posts):
        """Gets links from post objects"""
        posts_links = []
        for post in posts:
            url = URL(post.get("href"))
            if url not in posts_links:
                posts_links.append(url)
        return posts_links

    async def get_post(self, session: ScrapeSession, url: URL, domain_obj: DomainItem, model=None):
        """Gets content for a given post url"""
        try:
            soup = await session.get_BS4(url)
            if not model:
                model = await make_title_safe(soup.select_one("a[class=sh-section__name]").get_text()) + " (NSFW.XXX)"
            post_name = await make_title_safe(soup.select_one("div[class=sh-section__content] p").get_text())

            content_obj = soup.select("div[class=sh-section__image] img")
            content_obj.extend(soup.select("video source"))
            content_obj.extend(soup.select('div[class="sh-section__images sh-section__images_gallery row"] div a img'))

            for content in content_obj:
                link = URL(content.get("src"))
                if "-mobile" in link.name or ".webm" in link.name:
                    continue
                complete = await self.SQL_Helper.check_complete_singular("nsfw.xxx", link)
                try:
                    filename, ext = await get_filename_and_ext(link.name)
                except NoExtensionFailure:
                    logger.debug("Couldn't get extension for %s", str(link))
                    continue
                media = MediaItem(link, url, complete, filename, ext, filename)

                title = f"{model}/{post_name}" if self.separate_posts else model
                await domain_obj.add_media(title, media)

        except Exception as e:
            logger.debug("Error encountered while handling %s", str(url), exc_info=True)
            await log(f"Error: {str(url)}", quiet=self.quiet, style="red")
            logger.debug(e)
