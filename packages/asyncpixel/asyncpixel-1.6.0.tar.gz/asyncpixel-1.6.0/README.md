<h1 align="center">
  Asyncpixel
</h1>

<h3 align="center">
  Easily access Hypixel's api
</h3>
<p align="center">
  Asyncpixel is an open source asynchronous python wrapper for the Hypixel api with 100% of all endpoints.
</p>

<h3 align="center">
 🤖 🎨 🚀
</h3>

<p align="center">
  <a href="https://github.com/Darkflame72/asyncpixel/releases">
    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/Darkflame72/asyncpixel/total">
  </a>
  <a href="https://github.com/Darkflame72/asyncpixel/releases">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/Darkflame72/asyncpixel">
  </a>
  <a href="https://github.com/Darkflame72/asyncpixel/actions?workflow=Tests">
  <img src="https://github.com/Darkflame72/asyncpixel/workflows/Tests/badge.svg" alt="Test status" />
  </a>
   <img src="https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg" alt="Code of conduct" />
</p>

<h3 align="center">
  <a href="https://asyncpixel.readthedocs.org">Docs</a>
  <span> · </span>
  <a href="https://github.com/Darkflame72/asyncpixel/discussions?discussions_q=category%3AIdeas">Feature request</a>
  <span> · </span>
  <a href="https://github.com/Darkflame72/asyncpixel/issues">Report a bug</a>
  <span> · </span>
  Support: <a href="https://github.com/Darkflame72/asyncpixel/discussions">Discussions</a>
</h3>

## ✨ Features

- **Asyncronous.** Unlike other libraries Asyncpixel is fully asynchronous. This makes it perfect to use in your next discord bot or powerful website without having to worry about blocking.

- **100% API coverage.** Asyncpixel is currently the only python library with full coverage of the Hypixel API meaning that no endpoints are left untouched and out of your reach.

- **Pydantic models.** All models are checked and validated by [Pydantic](https://github.com/samuelcolvin/pydantic) meaning that the data is always in the correct format perfect for you to use.

- **Available on pypi.** Asyncpixel is available on pypi meaning no building from source, just use `pip install asyncpixel` to use it in your project.

## 🏁 Getting Started with Asyncpixel

To get started check out the documentation which [lives here](https://asyncpixel.readthedocs.org) and is generously hosted by readthedocs.

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) or your favourite tool to install asyncpixel.

```bash
pip install asyncpixel
```

### Example

```python
import asyncpixel
import asyncio

async def main():
  hypixel = asyncpixel.Hypixel("hypixel_api_key")
  player = await hypixel.player("405dcf08b80f4e23b97d943ad93d14fd")
  print(player.stats.bedwars)
  await hypixel.close()


asyncio.run(main())
```

## ❗ Code of Conduct

Darkflame72 is dedicated to providing a welcoming, diverse, and harassment-free experience for everyone. We expect everyone in the Darkflame72 community to abide by our [**Code of Conduct**](https://github.com/Darkflame72/asyncpixel/blob/main/CODE_OF_CONDUCT.rst). Please read it.

## 🙌 Contributing to Asyncpixel

From opening a bug report to creating a pull request: every contribution is appreciated and welcomed. If you are planning to implement a new feature or change the library please create an issue first. This way we can ensure your work is not in vain.

### Not Sure Where to Start?

A good place to start contributing, are the [Good first issues](https://github.com/Darkflame72/asyncpixel/labels/good%20first%20issue).

## 📝 License

Asyncpixel is open-source. The library is licensed [GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html).

## 💬 Get in touch

If you have a question or would like to talk with other Asyncpixel users, please hop over to [Github discussions](https://github.com/Darkflame72/asyncpixel/discussions).

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://quirky.codes/"><img src="https://avatars2.githubusercontent.com/u/35202521?v=4?s=100" width="100px;" alt="AjayACST"/><br /><sub><b>AjayACST</b></sub></a><br /><a href="#maintenance-AjayACST" title="Maintenance">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aiexz"><img src="https://avatars3.githubusercontent.com/u/42418433?v=4?s=100" width="100px;" alt="Alex"/><br /><sub><b>Alex</b></sub></a><br /><a href="https://github.com/Darkflame72/asyncpixel/commits?author=aiexz" title="Code">💻</a> <a href="https://github.com/Darkflame72/asyncpixel/issues?q=author%3Aaiexz" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/magicaltoast"><img src="https://avatars.githubusercontent.com/u/68669235?v=4?s=100" width="100px;" alt="Damian Grzanka"/><br /><sub><b>Damian Grzanka</b></sub></a><br /><a href="https://github.com/Darkflame72/asyncpixel/commits?author=magicaltoast" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/satyamedh"><img src="https://avatars.githubusercontent.com/u/47636284?v=4?s=100" width="100px;" alt="satyamedh hulyalkar"/><br /><sub><b>satyamedh hulyalkar</b></sub></a><br /><a href="https://github.com/Darkflame72/asyncpixel/issues?q=author%3Asatyamedh" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://dubs.rip"><img src="https://avatars.githubusercontent.com/u/59372145?v=4?s=100" width="100px;" alt="dubs"/><br /><sub><b>dubs</b></sub></a><br /><a href="https://github.com/Darkflame72/asyncpixel/issues?q=author%3Aduhby" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Amund211"><img src="https://avatars.githubusercontent.com/u/14028449?v=4?s=100" width="100px;" alt="Amund Eggen Svandal"/><br /><sub><b>Amund Eggen Svandal</b></sub></a><br /><a href="https://github.com/Darkflame72/asyncpixel/commits?author=Amund211" title="Code">💻</a> <a href="https://github.com/Darkflame72/asyncpixel/issues?q=author%3AAmund211" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/wald0040"><img src="https://avatars.githubusercontent.com/u/88714744?v=4?s=100" width="100px;" alt="wald0040"/><br /><sub><b>wald0040</b></sub></a><br /><a href="https://github.com/Darkflame72/asyncpixel/issues?q=author%3Awald0040" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MillionthOdin16"><img src="https://avatars.githubusercontent.com/u/102247808?v=4?s=100" width="100px;" alt="MillionthOdin16"/><br /><sub><b>MillionthOdin16</b></sub></a><br /><a href="https://github.com/Darkflame72/asyncpixel/issues?q=author%3AMillionthOdin16" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ch-iv"><img src="https://avatars.githubusercontent.com/u/108201575?v=4?s=100" width="100px;" alt="ch-iv"/><br /><sub><b>ch-iv</b></sub></a><br /><a href="https://github.com/Darkflame72/asyncpixel/issues?q=author%3Ach-iv" title="Bug reports">🐛</a> <a href="https://github.com/Darkflame72/asyncpixel/commits?author=ch-iv" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind are welcome!
