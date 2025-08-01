#!/usr/bin/env python3
"""Configuration settings for the OpenAI Arcade Agent."""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AgentConfig:
    """Configuration class for the OpenAI Arcade Agent."""

    # API Keys
    ARCADE_API_KEY = os.getenv("ARCADE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ARCADE_USER_ID = os.getenv("ARCADE_USER_ID", "hi@lewismenelaws.com")

    # Agent Settings
    DEFAULT_MODEL = "gpt-4o-mini"
    ALTERNATIVE_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"]

    # Default Toolkits
    DEFAULT_TOOLKITS = ["gmail", "math"]

    # Available Toolkits
    AVAILABLE_TOOLKITS = [
        "gmail",  # Email management
        "math",  # Mathematical calculations
        "github",  # Git repository management
        "linkedin",  # Professional networking
        "slack",  # Team communication
        "calendar",  # Event scheduling
        "notion",  # Workspace management
        "asana",  # Project management
        "stripe",  # Payment processing
        "salesforce",  # CRM management
        "discord",  # Community chat
        "twitter",  # Social media
        "shopify",  # E-commerce
    ]

    # Toolkit Descriptions
    TOOLKIT_DESCRIPTIONS = {
        "gmail": "📧 Email: Read, search, send, and manage Gmail messages",
        "math": "🔢 Math: Perform calculations, solve equations, and mathematical operations",
        "github": "🐙 GitHub: Manage repositories, issues, pull requests, and code",
        "linkedin": "💼 LinkedIn: Access professional network and career data",
        "slack": "💬 Slack: Send messages, manage channels, and team communication",
        "calendar": "📅 Calendar: Schedule events, manage appointments, and time planning",
        "notion": "📝 Notion: Access workspace, databases, and knowledge management",
        "asana": "✅ Asana: Manage projects, tasks, and team collaboration",
        "stripe": "💳 Stripe: Handle payments, customers, and financial transactions",
        "salesforce": "🏢 Salesforce: CRM operations, leads, and customer management",
        "discord": "🎮 Discord: Community chat, server management, and messaging",
        "twitter": "🐦 Twitter: Social media posting, engagement, and content management",
        "shopify": "🛒 Shopify: E-commerce, products, orders, and store management",
    }

    # Printing Settings
    AUTO_PRINT = True
    PRINT_SUCCESS_MESSAGES = True
    SAVE_PDF_COPIES = True

    # Priority Mappings
    PRIORITY_KEYWORDS = {
        "HIGH": ["urgent", "critical", "important", "asap", "priority", "deadline"],
        "MEDIUM": ["task", "todo", "action", "follow-up", "reminder"],
        "LOW": ["info", "fyi", "reference", "note", "update"],
    }

    @classmethod
    def get_toolkit_description(cls, toolkit_name: str) -> str:
        """Get description for a toolkit."""
        return cls.TOOLKIT_DESCRIPTIONS.get(
            toolkit_name, f"📦 {toolkit_name.title()}: Third-party toolkit"
        )

    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        missing = []

        if not cls.ARCADE_API_KEY:
            missing.append("ARCADE_API_KEY")

        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")

        if missing:
            print("❌ Missing required environment variables:")
            for var in missing:
                print(f"   - {var}")
            print("\nPlease set these in your .env file or environment.")
            return False

        return True

    @classmethod
    def show_config_info(cls):
        """Display current configuration information."""
        print("🔧 AGENT CONFIGURATION")
        print("=" * 50)
        print(f"Model: {cls.DEFAULT_MODEL}")
        print(f"User ID: {cls.ARCADE_USER_ID}")
        print(f"Auto Print: {cls.AUTO_PRINT}")
        print(f"Save PDFs: {cls.SAVE_PDF_COPIES}")
        print(f"Default Toolkits: {', '.join(cls.DEFAULT_TOOLKITS)}")
        print(f"Available Toolkits: {len(cls.AVAILABLE_TOOLKITS)}")

        print("\n📦 AVAILABLE TOOLKITS:")
        for toolkit in cls.AVAILABLE_TOOLKITS:
            print(f"   {cls.get_toolkit_description(toolkit)}")

        # Check API keys (without revealing them)
        print("\n🔑 API KEYS:")
        print(f"   Arcade API Key: {'✅ Set' if cls.ARCADE_API_KEY else '❌ Missing'}")
        print(f"   OpenAI API Key: {'✅ Set' if cls.OPENAI_API_KEY else '❌ Missing'}")


# Preset configurations for different use cases
class PresetConfigs:
    """Predefined configurations for common use cases."""

    EMAIL_ASSISTANT = {
        "toolkits": ["gmail", "calendar"],
        "instructions": "You are an email assistant. Help manage emails, schedule meetings, and organize communications. Always prioritize urgent messages and provide clear summaries.",
    }

    DEVELOPER_ASSISTANT = {
        "toolkits": ["github", "slack", "notion"],
        "instructions": "You are a developer assistant. Help with code repositories, team communication, and project documentation. Focus on code quality and team collaboration.",
    }

    BUSINESS_ASSISTANT = {
        "toolkits": ["salesforce", "stripe", "asana", "linkedin"],
        "instructions": "You are a business assistant. Help with customer management, payments, project tracking, and professional networking. Focus on efficiency and business growth.",
    }

    SOCIAL_MEDIA_MANAGER = {
        "toolkits": ["twitter", "linkedin", "discord"],
        "instructions": "You are a social media manager. Help create engaging content, manage communities, and build professional networks. Focus on audience engagement and brand building.",
    }

    ECOMMERCE_ASSISTANT = {
        "toolkits": ["shopify", "stripe", "gmail"],
        "instructions": "You are an e-commerce assistant. Help manage online stores, process orders, handle payments, and communicate with customers. Focus on customer satisfaction and sales optimization.",
    }

    GENERAL_ASSISTANT = {
        "toolkits": ["gmail", "math", "calendar", "notion"],
        "instructions": "You are a general assistant. Help with various tasks including email management, calculations, scheduling, and note-taking. Adapt to the user's needs and provide helpful insights.",
    }


if __name__ == "__main__":
    # Show configuration when run directly
    AgentConfig.show_config_info()
    print(f"\nConfiguration valid: {AgentConfig.validate_config()}")
