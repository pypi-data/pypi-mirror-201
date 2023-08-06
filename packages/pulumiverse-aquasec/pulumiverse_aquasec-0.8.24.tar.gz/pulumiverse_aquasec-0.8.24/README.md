# Aquasec Resource Provider

The Aquasec Resource Provider lets you manage [Aquasec](https://www.aquasec.com/) resources.

## Installing

This package is available for several languages/platforms:

### Node.js (JavaScript/TypeScript)

To use from JavaScript or TypeScript in Node.js, install using either `npm`:

```bash
npm install @pulumiverse/aquasec
```

or `yarn`:

```bash
yarn add @pulumiverse/aquasec
```

### Python

To use from Python, install using `pip`:

```bash
pip install pulumiverse_aquasec
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/pulumiverse/pulumi-aquasec/sdk/go/...
```

### .NET

To use from .NET, install using `dotnet add package`:

```bash
dotnet add package Pulumiverse.Aquasec
```

## Configuration

The following configuration points are available for the `aquasec` provider:

- `aquasec:username` (environment: `AQUA_USER`) - This is the user id that should be used to make the connection.
- `aquasec:password` (environment: `AQUA_PASSWORD`) - This is the password that should be used to make the connection.
- `aquasec:aqua_url` (environment: `AQUA_URL`) - This is the base URL of your Aqua instance.

## Reference

For detailed reference documentation, please visit [the Pulumi registry](https://www.pulumi.com/registry/packages/aquasec/api-docs/).
