# coding: utf-8
from __future__ import unicode_literals

import re
from .common import InfoExtractor
from ..utils import parse_duration, merge_dicts


class MallTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?mall\.tv/(?:.+/)?(?P<id>.+)(?:\?.*$|$)'
    _TESTS = [
        {
            'url': 'https://www.mall.tv/18-miliard-pro-neziskovky-opravdu-jsou-sportovci-nebo-clovek-v-tisni-pijavice',
            'md5': '9ced0de056534410837077e23bfba796',
            'info_dict': {
                'id': 't0zzt0',
                'ext': 'mp4',
                'title': '18 miliard pro neziskovky. Opravdu jsou sportovci nebo Člověk v tísni pijavice?',
                'description': 'Pokud někdo hospodaří s penězmi daňových poplatníků, pak logicky chceme vědět, jak s nimi nakládá. Objem dotací pro neziskovky roste, ale opravdu jsou tyto organizace „pijavice", jak o nich hovoří And',
                'upload_date': '20181007',
                'timestamp': 1538870400
                }
        },
        {
            'url': 'https://www.mall.tv/kdo-to-plati/18-miliard-pro-neziskovky-opravdu-jsou-sportovci-nebo-clovek-v-tisni-pijavice',
            'md5': '9ced0de056534410837077e23bfba796',
            'only_matching': 1,
            'info_dict': {
                'id': 't0zzt0',
                'ext': 'mp4',
                'title': '18 miliard pro neziskovky. Opravdu jsou sportovci nebo Člověk v tísni pijavice?',
                'description': 'Pokud někdo hospodaří s penězmi daňových poplatníků, pak logicky chceme vědět, jak s nimi nakládá. Objem dotací pro neziskovky roste, ale opravdu jsou tyto organizace „pijavice", jak o nich hovoří And',
                'upload_date': '20181007',
                'timestamp': 1538870400
                }
        }
    ]

    def _real_extract(self, url):
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)
        src_id_regex = r'(?P<src><source src=([\"\'])?.+?/(?P<id>\w{6,}?)/index)(?P<after>\1?[^>]*?>)'
        video_id = self._search_regex(src_id_regex, webpage, 'ID',
                                           group='id')
        info = self._search_json_ld(webpage, video_id, default={})
        html = re.sub(src_id_regex, r'\g<src>.m3u8\g<after>', webpage)
        media = self._parse_html5_media_entries(url, html, video_id)
        thumbnail = info.get('thumbnail', self._og_search_thumbnail(webpage))
        duration = parse_duration(info.get('duration'))
        result = {
            'id': video_id,
            'title': info.get('title', self._og_search_title(webpage)),
            'description': self._og_search_description(webpage)
        }
        result.update({'thumbnail': thumbnail})
        result.update({'duration': duration})

        return merge_dicts(media[0], info, result)
