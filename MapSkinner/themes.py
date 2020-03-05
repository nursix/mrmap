from django.utils.html import format_html
ICON_PATTERN = "<i class=\'{} {}\'></i>"

FONT_AWESOME_ICONS = {
    'DASHBOARD': format_html(ICON_PATTERN, 'fas', 'fa-tachometer-alt', ),
    'WMS': format_html(ICON_PATTERN, 'far', 'fa-map', ),
    'WMS_SOLID': format_html(ICON_PATTERN, 'fas', 'fa-map', ),
    'WFS': format_html(ICON_PATTERN, 'fas', 'fa-draw-polygon', ),
    'LAYER': format_html(ICON_PATTERN, 'fas', 'fa-layer-group', ),
    'DATASET': format_html(ICON_PATTERN, 'fas', 'fa-clipboard-list', ),
    'PENDINGTASKS': format_html(ICON_PATTERN, 'fas', 'fa-tasks', ),
    'USER': format_html(ICON_PATTERN, 'fas', 'fa-user', ),
    'PASSWORD': format_html(ICON_PATTERN, 'fas', 'fa-lock', ),
    'GROUP': format_html(ICON_PATTERN, 'fas', 'fa-users', ),
    'ORGANIZATION': format_html(ICON_PATTERN, 'fas', 'fa-building', ),
    'UPDATE': format_html(ICON_PATTERN, 'fas', 'fa-spinner', ),
    'REMOVE': format_html(ICON_PATTERN, 'fas', 'fa-trash', ),
    'SEARCH': format_html(ICON_PATTERN, 'fas', 'fa-search', ),
    'RETURN': format_html(ICON_PATTERN, 'fas', 'fa-arrow-circle-left', ),
    'ADD': format_html(ICON_PATTERN, 'fas', 'fa-plus-circle', ),
    'OK': format_html(ICON_PATTERN, 'fas', 'fa-check', ),
    'NOK': format_html(ICON_PATTERN, 'fas', 'fa-times', ),
    'OK_CIRCLE': format_html(ICON_PATTERN, 'far', 'fa-check-circle', ),
    'NOK_CIRCLE': format_html(ICON_PATTERN, 'far', 'fa-times-circle', ),
    'EDIT': format_html(ICON_PATTERN, 'fas', 'fa-edit', ),
    'SIGNOUT': format_html(ICON_PATTERN, 'fas', 'fa-sign-out-alt', ),
    'SIGNIN': format_html(ICON_PATTERN, 'fas', 'fa-sign-in-alt', ),
    'SIGNUP': format_html(ICON_PATTERN, 'fas', 'fa-user-plus', ),
    'UNDO': format_html(ICON_PATTERN, 'fas', 'fa-undo', ),
    'CAPABILITIES': format_html(ICON_PATTERN, 'fas', 'fa-file-code', ),
    'METADATA': format_html(ICON_PATTERN, 'fas', 'fa-file-alt', ),
    'ACCESS': format_html(ICON_PATTERN, 'fas', 'fa-key', ),
    'SORT_ALPHA_UP': format_html(ICON_PATTERN, 'fas', 'fa-sort-alpha-up', ),
    'SORT_ALPHA_DOWN': format_html(ICON_PATTERN, 'fas', 'fa-sort-alpha-down', ),
    'ACTIVITY': format_html(ICON_PATTERN, 'fas', 'fa-snowboarding', ),
    'HISTORY': format_html(ICON_PATTERN, 'fas', 'fa-history', ),
    'SERVICE': format_html(ICON_PATTERN, 'fas', 'fa-concierge-bell', ),
    'SAVE': format_html(ICON_PATTERN, 'fas', 'fa-save', ),
    'UPLOAD': format_html(ICON_PATTERN, 'fas', 'fa-upload', ),
    'DOWNLOAD': format_html(ICON_PATTERN, 'fas', 'fa-download', ),
    'SEND_EMAIL': format_html(ICON_PATTERN, 'fas', 'fa-envelope-open-text', ),
    'WINDOW_CLOSE': format_html(ICON_PATTERN, 'fas', 'fa-window-close', ),
    'HIERARCHY': format_html(ICON_PATTERN, 'fas', 'fa-sitemap', ),
    'GLOBE': format_html(ICON_PATTERN, 'fas', 'fa-globe', ),
    'LINK': format_html(ICON_PATTERN, 'fas', 'fa-link', ),
    'EXTERNAL_LINK': format_html(ICON_PATTERN, 'fas', 'fa-external-link-alt', ),
    'PUBLISHER': format_html(ICON_PATTERN, 'fas', 'fa-address-card', ),
}

# dark theme settings
DARK_THEME = {
    'NAME': 'dark',

    'BACKGROUND': 'bg-secondary',
    'BACKGROUND_IMG': 'bg-img dark-theme',

    'TXT_DEF_COLOR': 'text-white',

    'TABLE': {
        'HOVER': 'table-hover',
        'STRIPED': 'table-striped',
        'BG': 'table-dark',
        'BOARDER': 'border border-white rounded',
        'LINK_COLOR': 'text-info',
        'LINK_COLOR_SUCCESS': 'text-success',
        'BORDERED': 'table-bordered',
        'BTN_PRIMARY_COLOR': 'btn-outline-info',
        'BTN_SECONDARY_COLOR': 'btn-outline-secondary',
        'BTN_SUCCESS_COLOR': 'btn-outline-success',
        'BTN_DANGER_COLOR': 'btn-outline-danger',
        'BTN_WARNING_COLOR': 'btn-outline-warning',
        'BTN_INFO_COLOR': 'btn-outline-primary',
        'PILL_BADGE_INFO_COLOR': 'badge-pill badge-info',
        'PILL_BADGE_LIGHT_COLOR': 'badge-pill badge-light',
    },

    'CARD': {
        'BG': 'bg-dark',
        'TXT_COLOR': 'text-white',
        'BOARDER': 'border border-white rounded',
        'LINK_COLOR': 'text-info',
        'BTN_PRIMARY_COLOR': 'btn-outline-info',
        'BTN_SECONDARY_COLOR': 'btn-outline-secondary',
        'BTN_SUCCESS_COLOR': 'btn-outline-success',
        'BTN_DANGER_COLOR': 'btn-outline-danger',
        'BTN_WARNING_COLOR': 'btn-outline-warning',
        'BTN_INFO_COLOR': 'btn-outline-primary',
        'BADGE_COLOR': 'badge-info',
        'BADGE_LIGHT': 'badge-light',
    },

    'NAV': {
        'ITEM_COLOR': 'navbar-dark',
        'BG_COLOR': 'bg-dark',
        'TXT_COLOR': 'text-white',
        'BTN_PRIMARY_COLOR': 'btn-outline-info',
        'BTN_SECONDARY_COLOR': 'btn-outline-secondary',
        'BTN_SUCCESS_COLOR': 'btn-outline-success',
        'BTN_DANGER_COLOR': 'btn-outline-danger',
        'BTN_WARNING_COLOR': 'btn-outline-warning',
        'BTN_INFO_COLOR': 'btn-outline-primary',
        'BTN_LIGHT': 'btn-outline-light',
    },

    'FOOTER': {
        'BG_COLOR': 'bg-dark',
        'TXT_COLOR': 'text-secondary',
        'LINK_COLOR': 'text-info',
        'BTN_PRIMARY_COLOR': 'btn-outline-info',
        'BTN_SECONDARY_COLOR': 'btn-outline-secondary',
        'BTN_SUCCESS_COLOR': 'btn-outline-success',
        'BTN_DANGER_COLOR': 'btn-outline-danger',
        'BTN_WARNING_COLOR': 'btn-outline-warning',
        'BTN_INFO_COLOR': 'btn-outline-primary',
        'BTN_LANGUAGE': 'btn-dark',
    },

    'MODAL': {
        'BG_COLOR': 'bg-dark',
        'TXT_COLOR': 'text-white',
        'BTN_PRIMARY_COLOR': 'btn-outline-info',
        'BTN_SECONDARY_COLOR': 'btn-outline-secondary',
        'BTN_SUCCESS_COLOR': 'btn-outline-success',
        'BTN_DANGER_COLOR': 'btn-outline-danger',
        'BTN_WARNING_COLOR': 'btn-outline-warning',
        'BTN_INFO_COLOR': 'btn-outline-primary',
    },

    'ACCORDION': {
        'BTN_PRIMARY_COLOR': 'btn-outline-info',
        'PILL_BADGE_INFO_COLOR': 'badge-pill badge-info',
    },

    'ICONS': FONT_AWESOME_ICONS,
}

# dark theme settings
LIGHT_THEME = {
    'NAME': 'light',
    'BACKGROUND': 'bg-light',
    'BACKGROUND_IMG': 'bg-img',

    'TXT_DEF_COLOR': 'text-dark',

    'TABLE': {
        'HOVER': 'table-hover',
        'STRIPED': 'table-striped',
        'BG': 'bg-light',
        'BOARDER': 'border border-dark rounded',
        'LINK_COLOR': 'text-primary',
        'LINK_COLOR_SUCCESS': 'text-success',
        'BORDERED': 'table-bordered',
        'BTN_PRIMARY_COLOR': 'btn-primary',
        'BTN_SECONDARY_COLOR': 'btn-secondary',
        'BTN_SUCCESS_COLOR': 'btn-success',
        'BTN_DANGER_COLOR': 'btn-danger',
        'BTN_WARNING_COLOR': 'btn-warning',
        'BTN_INFO_COLOR': 'btn-info',
        'PILL_BADGE_INFO_COLOR': 'badge-pill badge-info',
        'PILL_BADGE_LIGHT_COLOR': 'badge-pill badge-light',
    },

    'CARD': {
        'BG': 'bg-light',
        'TXT_COLOR': ' ',
        'BOARDER': 'border border-dark rounded',
        'LINK_COLOR': 'text-primary',
        'BTN_PRIMARY_COLOR': 'btn-primary',
        'BTN_SECONDARY_COLOR': 'btn-secondary',
        'BTN_SUCCESS_COLOR': 'btn-success',
        'BTN_DANGER_COLOR': 'btn-danger',
        'BTN_WARNING_COLOR': 'btn-warning',
        'BTN_INFO_COLOR': 'btn-info',
        'BADGE_COLOR': 'badge-primary',
        'BADGE_LIGHT': 'badge-light',
    },

    'NAV': {
        'ITEM_COLOR': 'navbar-light',
        'BG_COLOR': 'bg-light',
        'TXT_COLOR': ' ',
        'BTN_PRIMARY_COLOR': 'btn-primary',
        'BTN_SECONDARY_COLOR': 'btn-secondary',
        'BTN_SUCCESS_COLOR': 'btn-success',
        'BTN_DANGER_COLOR': 'btn-danger',
        'BTN_WARNING_COLOR': 'btn-warning',
        'BTN_INFO_COLOR': 'btn-info',
        'BTN_LIGHT': 'btn-outline-light',
    },

    'FOOTER': {
        'BG_COLOR': 'bg-light',
        'TXT_COLOR': ' ',
        'LINK_COLOR': 'text-primary',
        'BTN_PRIMARY_COLOR': 'btn-primary',
        'BTN_SECONDARY_COLOR': 'btn-secondary',
        'BTN_SUCCESS_COLOR': 'btn-success',
        'BTN_DANGER_COLOR': 'btn-danger',
        'BTN_WARNING_COLOR': 'btn-warning',
        'BTN_INFO_COLOR': 'btn-primary',
        'BTN_LANGUAGE': 'btn-light',
    },

    'MODAL': {
        'BG_COLOR': 'bg-light',
        'TXT_COLOR': ' ',
        'BTN_PRIMARY_COLOR': 'btn-primary',
        'BTN_SECONDARY_COLOR': 'btn-secondary',
        'BTN_SUCCESS_COLOR': 'btn-success',
        'BTN_DANGER_COLOR': 'btn-danger',
        'BTN_WARNING_COLOR': 'btn-warning',
        'BTN_INFO_COLOR': 'btn-info',
    },

    'ACCORDION': {
        'BTN_COLOR': 'btn-info',
        'PILL_BADGE_INFO_COLOR': 'badge-pill badge-info',
        'PILL_BADGE_LIGHT_COLOR': 'badge-pill badge-light',
    },

    'ICONS': FONT_AWESOME_ICONS,
}
