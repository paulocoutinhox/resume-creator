from modules.models.enums import IconKey, SocialNetwork


# lucide icon paths (https://lucide.dev) rendered as inline svg with stroke="currentColor".
_ICON_BODIES: dict[IconKey, str] = {
    IconKey.PHONE: '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.72 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.35 1.85.59 2.81.72A2 2 0 0 1 22 16.92Z"/>',
    IconKey.WHATSAPP: '<path d="M3 21l1.65-4.5A8.5 8.5 0 1 1 7.5 19.35L3 21Z"/><path d="M8.5 9.5c.5 2 2 3.5 4 4l1-1.2a1 1 0 0 1 1.05-.32l2.2.7a1 1 0 0 1 .68 1.08l-.2 1.2a1.5 1.5 0 0 1-1.6 1.24c-3.6-.2-6.55-3.15-6.75-6.75A1.5 1.5 0 0 1 10.12 7.8l1.2-.2a1 1 0 0 1 1.08.68l.7 2.2a1 1 0 0 1-.32 1.05L11.6 12.5"/>',
    IconKey.MAIL: '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    IconKey.MAP_PIN: '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    IconKey.USER: '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    IconKey.LINKEDIN: '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6Z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
    IconKey.GITHUB: '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.4 5.4 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>',
    IconKey.GLOBE: '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    IconKey.YOUTUBE: '<path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
    IconKey.INSTAGRAM: '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
    IconKey.X: '<path d="M4 4l16 16"/><path d="M20 4 4 20"/>',
    IconKey.BRIEFCASE: '<rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    IconKey.GRADUATION_CAP: '<path d="M22 10v6"/><path d="M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 1.66 3.13 3 6 3s6-1.34 6-3v-5"/>',
    IconKey.AWARD: '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
    IconKey.LANGUAGES: '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    IconKey.LIGHTBULB: '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    IconKey.SPARKLES: '<path d="M9.94 14.06 12 22l2.06-7.94L22 12l-7.94-2.06L12 2 9.94 9.94 2 12z"/>',
    IconKey.EXTERNAL_LINK: '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    IconKey.BUILDING: '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
    IconKey.CALENDAR: '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
}


_SOCIAL_ICON: dict[SocialNetwork, IconKey] = {
    SocialNetwork.LINKEDIN: IconKey.LINKEDIN,
    SocialNetwork.GITHUB: IconKey.GITHUB,
    SocialNetwork.SITE: IconKey.GLOBE,
    SocialNetwork.YOUTUBE: IconKey.YOUTUBE,
    SocialNetwork.INSTAGRAM: IconKey.INSTAGRAM,
    SocialNetwork.X: IconKey.X,
}


def render_icon(key: IconKey, css_class: str = "icon", stroke: str = "currentColor") -> str:
    body = _ICON_BODIES[key]
    return (
        f'<svg class="{css_class}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        f'fill="none" stroke="{stroke}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


def social_icon_key(network: SocialNetwork) -> IconKey:
    return _SOCIAL_ICON[network]
