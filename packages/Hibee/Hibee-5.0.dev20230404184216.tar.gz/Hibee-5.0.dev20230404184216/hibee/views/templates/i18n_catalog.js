{% autoescape off %}
'use strict';
{
  const globals = this;
  const hibee = globals.hibee || (globals.hibee = {});

  {% if plural %}
  hibee.pluralidx = function(n) {
    const v = {{ plural }};
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  {% else %}
  hibee.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  {% endif %}

  /* gettext library */

  hibee.catalog = hibee.catalog || {};
  {% if catalog_str %}
  const newcatalog = {{ catalog_str }};
  for (const key in newcatalog) {
    hibee.catalog[key] = newcatalog[key];
  }
  {% endif %}

  if (!hibee.jsi18n_initialized) {
    hibee.gettext = function(msgid) {
      const value = hibee.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    hibee.ngettext = function(singular, plural, count) {
      const value = hibee.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[hibee.pluralidx(count)] : value;
      }
    };

    hibee.gettext_noop = function(msgid) { return msgid; };

    hibee.pgettext = function(context, msgid) {
      let value = hibee.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    hibee.npgettext = function(context, singular, plural, count) {
      let value = hibee.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = hibee.ngettext(singular, plural, count);
      }
      return value;
    };

    hibee.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    hibee.formats = {{ formats_str }};

    hibee.get_format = function(format_type) {
      const value = hibee.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = hibee.pluralidx;
    globals.gettext = hibee.gettext;
    globals.ngettext = hibee.ngettext;
    globals.gettext_noop = hibee.gettext_noop;
    globals.pgettext = hibee.pgettext;
    globals.npgettext = hibee.npgettext;
    globals.interpolate = hibee.interpolate;
    globals.get_format = hibee.get_format;

    hibee.jsi18n_initialized = true;
  }
};
{% endautoescape %}
