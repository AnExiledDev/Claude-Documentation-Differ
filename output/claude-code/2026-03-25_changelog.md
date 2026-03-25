# Claude Code Documentation Changes — 2026-03-25

## Summary

Two pages were modified in this update. The quickstart page received a large addition (+608 lines) in the form of an interactive installation configurator React component, surfacing install commands for all supported platforms and IDEs in one place. The keybindings page received a minor but functionally meaningful update: `Ctrl+M` is now documented as a reserved shortcut that cannot be rebound.

## Significant Changes

### Features

- **Interactive Install Configurator added to Quickstart**: The quickstart page now embeds a full React component (`InstallConfigurator`) that renders a tabbed, OS-aware installation widget. The component covers four installation targets (Terminal, Desktop, VS Code, JetBrains) and within the Terminal tab, four install methods:

  | Method | Command |
  |--------|---------|
  | macOS / Linux | `curl -fsSL https://claude.ai/install.sh \| bash` |
  | Windows (PowerShell) | `irm https://claude.ai/install.ps1 \| iex` |
  | Windows (CMD) | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` |
  | Homebrew | `brew install --cask claude-code` |
  | WinGet | `winget install Anthropic.ClaudeCode` |

  The component auto-detects the user's OS via `navigator.userAgent` and pre-selects the relevant install tab on page load.

  - *Implication*: Homebrew and WinGet users are explicitly warned that these package managers do not auto-update Claude Code; users must periodically run `brew upgrade claude-code` or `winget upgrade Anthropic.ClaudeCode` manually. Windows users can toggle between PowerShell and CMD installer variants within the same tab.
  - *Source*: [Quickstart](https://code.claude.com/docs/en/quickstart.md)

- **Team/Enterprise install path in the configurator**: The new widget includes a toggle — "I'm buying for a team or company (SSO, AWS/Azure/GCP, central billing)" — that reveals team-specific setup options. When enabled, a provider selector appears with four choices: Anthropic, Amazon Bedrock, Microsoft Foundry, and Google Vertex AI. Selecting a cloud provider surfaces a contextual setup notice, for example:

  > **Configure your AWS account first.** Running on Bedrock requires model access enabled in the AWS console and IAM credentials.

  Similar notices appear for Vertex AI (GCP project and service account setup) and Microsoft Foundry (Azure subscription with Foundry resource and model deployments).

  - *Implication*: The quickstart now serves as a unified entry point for both individual developers and enterprise teams deploying via cloud provider infrastructure, with direct links to the Bedrock, Vertex AI, and Foundry setup guides from the first page a new user visits.
  - *Source*: [Quickstart](https://code.claude.com/docs/en/quickstart.md)

### Configuration

- **`Ctrl+M` added to the reserved shortcuts list**: The keybindings documentation now lists `Ctrl+M` in the "Reserved shortcuts" table — shortcuts that cannot be rebound regardless of keybindings configuration.

  > | Ctrl+M | Identical to Enter in terminals (both send CR) |

  - *Implication*: At the terminal protocol level, `Ctrl+M` and `Enter` both emit a carriage return (CR), making them indistinguishable to applications. Developers attempting to bind a custom action to `Ctrl+M` would encounter confusing behavior; this entry clarifies why such a binding is not permitted.
  - *Source*: [Keybindings](https://code.claude.com/docs/en/keybindings.md)

## Notable Details

- The quickstart configurator is written as inline JSX/React directly in the Markdown source file. Copy-to-clipboard functionality includes a fallback using `document.execCommand('copy')` for environments where the Clipboard API is unavailable, with a 1800ms visual "Copied" confirmation state.
- VS Code extension install is documented both as a Marketplace link and as a CLI command: `code --install-extension anthropic.claude-code`.
- The JetBrains plugin URL in the configurator (`https://plugins.jetbrains.com/plugin/27310-claude-code-beta-`) still carries a `-beta-` suffix, indicating the JetBrains plugin remains in beta status.
- The configurator CSS includes full dark mode support toggled via a `.dark` class on a parent element, consistent with the documentation site's theming approach.

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `quickstart.md` | Modified | +608 / -0 | Added interactive `InstallConfigurator` React component with OS-aware install tabs for Terminal, Desktop, VS Code, and JetBrains, plus team/enterprise cloud provider selection |
| `keybindings.md` | Modified | +5 / -4 | Added `Ctrl+M` to the reserved shortcuts table (identical to Enter at the terminal level; cannot be rebound) |

---
*Generated from Claude Code CLI documentation changes detected on 2026-03-25*
