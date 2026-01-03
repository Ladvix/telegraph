import aiohttp
from typing import Any, List, Dict
from .types import Account, NodeElement, Page, PageViews


class TelegraphException(Exception):
    pass

class Telegraph():
    '''
    Async wrapper for Telegraph API.
    '''
    def __init__(
        self,
        access_token: str | None = None
    ):
        self.base_url = 'https://api.telegra.ph/'
        self.access_token = access_token

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=10)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if not self.session:
            raise RuntimeError('Session is not initialized. Use "async with Telegraph(...)" or pass a session.')
        
        if method != 'createAccount':
            if self.access_token:
                params['access_token'] = self.access_token

        async with self.session.post(f'{self.base_url}/{method}', json=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise aiohttp.ClientResponseError(
                    request_info=resp.request_info,
                    history=resp.history,
                    status=resp.status,
                    message=f'HTTP {resp.status}: {text}',
                    headers=resp.headers,
                )
            
            data = await resp.json()
            if not data['ok']:
                error = data['error']
                raise TelegraphException(f'API Error: {error}')

            return data['result']

    async def create_account(
        self,
        short_name: str,
        author_name: str,
        author_url: str
    ) -> Account:
        '''
        Use this method to create a new Telegraph account.

        See http://telegra.ph/api#createAccount.

        :param short_name: Required. Account name, helps users with several accounts remember
            which they are currently using. Displayed to the user above the 'Edit/Publish'
            button on Telegra.ph, other users don't see this name.
        :type short_name: str
        :param author_name: Default author name used when creating new articles.
        :type author_name: str
        :param author_url: Default profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :type author_url: str
        :return: On success, returns an Account object with the regular fields and an additional access_token field.
        :rtype: Account
        '''
        params = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        data = await self._request('createAccount', params)
        account = Account(**data)
        self.access_token = account.access_token
        return account

    async def create_page(
        self,
        title: str,
        content: List[NodeElement],
        author_name: str | None = None,
        author_url: str | None = None,
        return_content: bool = False
    ) -> Page:
        '''
        Use this method to create a new Telegraph page.

        See http://telegra.ph/api#createPage.
        
        :param title: Page title.
        :type title: str
        :param content: Content of the page.
        :type content: list[NodeElement]
        :param author_name: Author name, displayed below the article's title.
        :type author_name: str | None
        :param author_url: Profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :type author_url: str | None
        :param return_content: If true, a content field will be returned in the Page object.
        :type return_content: bool
        :return: On success, returns a Page object.
        :rtype: Page
        '''
        content = [node.as_dict() for node in content]
        params = {
            'access_token': self.access_token,
            'title': title,
            'content': content,
            'author_name': author_name,
            'author_url': author_url,
            'return_content': return_content
        }
        data = await self._request('createPage', params)
        page = Page(**data)
        return page

    async def edit_account_info(
        self,
        short_name: str | None = None,
        author_name: str | None = None,
        author_url: str | None = None
    ) -> Account:
        '''
        Use this method to update information about a Telegraph account.

        See http://telegra.ph/api#editAccountInfo.
        
        :param short_name: New account name.
        :type short_name: str
        :param author_name: New default author name used when creating new articles.
        :type author_name: str
        :param author_url: New default profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :type author_url: str
        :return: On success, returns an Account object with the default fields.
        :rtype: Account
        '''
        params = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        data = await self._request('editAccountInfo', params)
        account = Account(**data)
        self.access_token = account.access_token
        return account

    async def edit_page(
        self,
        path: str,
        title: str,
        content: List[NodeElement],
        author_name: str | None = None,
        author_url: str | None = None,
        return_content: bool = False
    ) -> Page:
        '''
        Use this method to edit an existing Telegraph page.

        See http://telegra.ph/api#editPage.
        
        :param path: Path to the page.
        :type path: str
        :param title: Page title.
        :type title: str
        :param content: Content of the page.
        :type content: list[NodeElement]
        :param author_name: Author name, displayed below the article's title.
        :type author_name: str | None
        :param author_url: Profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :type author_url: str | None
        :param return_content: If true, a content field will be returned in the Page object.
        :type return_content: bool
        :return: On success, returns a Page object.
        :rtype: Page
        '''
        content = [node.as_dict() for node in content]
        params = {
            'path': path,
            'title': title,
            'content': content,
            'author_name': author_name,
            'author_url': author_url,
            'return_content': return_content
        }
        data = await self._request('editPage', params)
        page = Page(**data)
        return page

    async def get_account_info(
        self,
        fields: List[str] | None = None
    ) -> Account:
        '''
        Use this method to get information about a Telegraph account.

        See http://telegra.ph/api#getAccountInfo.

        :param fields: List of account fields to return. Available fields: short_name, author_name, author_url, auth_url, page_count.
        :type fields: list[str]
        :return: Returns an Account object on success.
        :rtype: Account
        '''
        params = {
            'fields': fields
        }
        data = await self._request('getAccountInfo', params)
        account = Account(**data)
        return account

    async def get_page(
        self,
        path: str,
        return_content: bool | None = None
    ) -> Page:
        '''
        Use this method to get a Telegraph page.

        See http://telegra.ph/api#getPage.

        :param path: Path to the Telegraph page (in the format Title-12-31, i.e. everything that comes after http://telegra.ph/).
        :type path: str
        :param return_content: If true, content field will be returned in Page object.
        :type return_content: bool
        :return: Returns a Page object on success.
        :rtype: Page
        '''
        params = {
            'path': path,
            'return_content': return_content
        }
        data = await self._request('getPage', params)
        page = Page(**data)
        return page

    async def get_page_list(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> List[Page]:
        '''
        Use this method to get a list of pages belonging to a Telegraph account.

        See http://telegra.ph/api#getPageList.
        
        :param offset: Sequential number of the first page to be returned.
        :type offset: int
        :param limit: Limits the number of pages to be retrieved.
            Must be a non-negative integer.
            Default is 0.
        :type limit: int
            Must be an integer between 0 and 200, inclusive.
            Default is 50.
        :return: Returns a PageList object, sorted by most recently created pages first.
        :rtype: list[Page]
        '''
        params = {
            'offset': offset,
            'limit': limit
        }
        data = await self._request('getPageList', params)
        pages = [Page(**page_data) for page_data in data['pages']]
        return pages

    async def get_views(
        self,
        path: str,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        hour: int | None = None
    ) -> PageViews:
        '''
        Use this method to get the number of views for a Telegraph article.

        See http://telegra.ph/api#getViews.
        
        :param path: Path to the Telegraph page (in the format Title-12-31,
            where 12 is the month and 31 the day the article was first published).
        :type path: str
        :param year: If passed, the number of page views for the requested year will be returned.
        :type year: int
        :param month: If passed, the number of page views for the requested month will be returned.
        :type month: int
        :param day: If passed, the number of page views for the requested day will be returned.
        :type day: int
        :param hour: If passed, the number of page views for the requested hour will be returned.
        :type hour: int
        :return: Returns a PageViews object on success. By default, the total number of page views will be returned.
        :rtype: PageViews
        '''
        params = {
            'year': year,
            'month': month,
            'day': day,
            'hour': hour
        }
        data = await self._request('getViews', params)
        views = PageViews(**data)
        return views

    async def revoke_access_token(
        self
    ) -> Account:
        '''
        Use this method to revoke access_token and generate a new one,
        for example, if the user would like to reset all connected sessions,
        or you have reasons to believe the token was compromised.

        See http://telegra.ph/api#revokeAccessToken.
        
        :return: On success, returns an Account object with new access_token and auth_url fields.
        :rtype: Account
        '''
        data = await self._request('getViews', {})
        account = Account(**data)
        return account