# ACML - Advanced Config Markup Language

ACML is a custom markup language designed for creating complex configuration files with nested sections and key-value pairs. It allows users to organize their configuration data into different subsections, making it easy to manage and modify large configuration files.

With ACML, you can easily define subsections using the [section.subsection] syntax, and populate them with any number of key-value pairs. These key-value pairs can be simple strings, integers, floats, lists, and even JSON-style dictionaries.

## Pros of ACML compared to INI:
- Supports nested subsections for better organization of configuration data
- Allows for multiple data types including lists and JSON-style dictionaries
- Easy to read and write, with a syntax that is similar to other markup languages
- Can be easily parsed using a variety of programming languages and tools

## Cons of ACML compared to INI:
- Requires users to learn a new syntax and language
- May be overkill for simple configuration files with only a few key-value pairs
- Some tools may not support ACML natively, requiring additional parsing or conversion steps

Overall, ACML is a powerful and flexible markup language for creating complex configuration files. If you need to manage large amounts of configuration data or need support for complex data types, ACML may be the right choice for you.

Example of a configuration file:

```javascript
[server]
host = localhost
port = 8080

[server.tls]
enabled = true
certfile = /path/to/cert.pem
keyfile = /path/to/key.pem
```

The resulting dictionary would be:

```json
{'server': {'host': 'localhost', 'port': '8080', 'tls': {'enabled': True, 'certfile': '/path/to/cert.pem', 'keyfile': '/path/to/key.pem'}}}
```