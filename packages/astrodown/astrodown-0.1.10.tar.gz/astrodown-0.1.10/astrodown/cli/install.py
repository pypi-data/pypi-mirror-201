import enum


class PackageManager(str, enum.Enum):
    npm = "npm"
    yarn = "yarn"
    pnpm = "pnpm"
