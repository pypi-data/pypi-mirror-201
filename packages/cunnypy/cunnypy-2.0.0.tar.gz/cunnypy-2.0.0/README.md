<h1 style="text-align:center">🦀 Cunny.py 🦀</h1>
<h3 style="text-align:center">🖼️ Python Bindings for Several Image Boards 🖼️</h3>
<p align="center">
    <a href="https://liberapay.com/GlitchyChan/donate">
        <img src="https://img.shields.io/badge/Liberapay-F6C915?style=for-the-badge&logo=liberapay&logoColor=black" alt="liberapay" />
    </a>
    <a href="https://discord.gg/ZxbYHEh">
        <img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=fff&style=for-the-badge" alt="Discord" />
    </a>
    <a href="https://twitter.com/glitchychan">
        <img src="https://img.shields.io/badge/twitter-%2300acee?&style=for-the-badge&logo=twitter&logoColor=white" alt="twitter" />
    </a>
</p>

---

<p align="center">
	<a href="#📜About">📜About</a> |
	<a href="#📥Installation">📥Installation</a> |
	<a href="#🌟Features">🌟Features</a> |
	<a href="#⚙️Usage">⚙️Usage</a>
</p>
<br>

## 📜About
🦀 Cunny.py is a library that makes it **dead-simple** to interact with image boards using Python.
<br>

## 📥Installation
✅ Getting started with Cunny.py is quick and easy! Simply install the package using your favorite tool.

📥Using [pip](https://pypi.org/project/pip/):

```bash
pip install cunnypy
```

🪶Using [poetry](https://python-poetry.org):

```bash
poetry add cunnypy
```
<br>

## 🌟Features
- 🚀 Fully Async
- 💯 Tons of boorus supported. See [Boorus.toml](./cunnypy/boorus.toml).
- 🆔 Support for booru aliases
- 🎲 Randomize each search with gatcha
- 🔍 Autocomplete support for tags
- 🔢 Search multiple boors at once
- 🐍 Modern and Pythonic API
<br>

## ⚙️Usage
🎉 Other examples can be found in the [Examples](./examples) folder.

### 🔎 Basic Search
📝 **Note**: You can specify additional parameters in the search function, such as `limit` and `gatcha`.

```python
import cunnypy
import asyncio


async def main():
    posts = await cunnypy.search("gelbooru", "megumin", limit=20, gatcha=True)
    print(posts)


asyncio.run(main())
```

### 🔍 Basic Multi-Booru Search

```python
import cunnypy
import asyncio

async def main():
    posts = await cunnypy.ms([{'booru': 'gel'}, {'booru': 'safe'}], "megumin")
    print(posts)

asyncio.run(main())
```

### 🤖 Autocomplete

```python
import cunnypy
import asyncio


async def main():
    auto = await cunnypy.autocomplete("gel", "megumi")
    print(auto)


asyncio.run(main())
```
