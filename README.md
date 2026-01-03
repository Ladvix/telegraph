# Telegraph

Async python wrapper for Telegraph

## Install

```bash
pip install async-wrapper-telegraph
```

## Usage

```py
import asyncio
from telegraph import Telegraph
from telegraph.types import NodeElement


async def main():
    access_token = 'd3b25feccb89e508a9114afb82aa421fe2a9712b963b387cc5ad71e58722'
    async with Telegraph(access_token) as client:
        r = await client.create_page(
            title='Test telegra.ph',
            content=[
                NodeElement(
                    tag='p',
                    children=[
                        'Hello, ',
                        NodeElement(tag='b', children=['world!'])
                    ]
                )
            ]
        )
        print(r)

asyncio.run(main())
```