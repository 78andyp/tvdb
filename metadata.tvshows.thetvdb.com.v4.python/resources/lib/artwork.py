import xbmcgui
import xbmcplugin

from .tvdb import Client, get_artworks_from_show, get_language

MAX_IMAGES_NUMBER = 10

def add_artworks(show, liz, language, max_season_images_number):
    
    artworks = get_artworks_from_show(show, language)
    fanarts = artworks.pop("fanarts")
    season_posters = artworks.pop("season_posters")

    for art_type, images in artworks.items():
        for image in images[:MAX_IMAGES_NUMBER]:
            liz.addAvailableArtwork(image['image'], art_type)
    
    season_posters_dict = {}
    for image, season_number in season_posters:
        season_posters_dict.setdefault(season_number, []).append(image)
    for season_number, images in season_posters_dict.items():
        for image in images[:max_season_images_number]:
            liz.addAvailableArtwork(image, 'poster', season=season_number)

    fanart_items = []
    for fanart in fanarts[:MAX_IMAGES_NUMBER]:
        fanart_items.append(
            {'image': fanart["image"], 'preview': fanart["thumbnail"]})
    liz.setAvailableFanart(fanart_items)


def get_artworks(id, settings, handle):
    tvdb_client = Client(settings)

    show = tvdb_client.get_series_details_api(id, settings)
    if not show:
        xbmcplugin.setResolvedUrl(
            handle, False, xbmcgui.ListItem(offscreen=True))
        return
    liz = xbmcgui.ListItem(id, offscreen=True)
    language = get_language(settings)
    max_season_images = int(settings.get("max_season_images"))
    add_artworks(show, liz, language, max_season_images)
    xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=liz)
