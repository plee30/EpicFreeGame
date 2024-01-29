from epicstore_api import EpicGamesStoreAPI
from datetime import datetime, timedelta, timezone

def get_promos():
    promos = {}
    cur = []
    fut = []
    """Fetches current free games from the store."""
    api = EpicGamesStoreAPI()
    free_games = api.get_free_games()['data']['Catalog']['searchStore']['elements']

    # Few odd items do not seems game and don't have the promotion attribute, so let's check it !
    free_games = list(sorted(
        filter(
            lambda g: g.get('promotions'),
            free_games
        ),
        key=lambda g: g['title']
    ))

    for game in free_games:
        game_title = game['title']
        game_url = f"https://store.epicgames.com/en-US/p/{game['catalogNs']['mappings'][0]['pageSlug']}"
        game_thumbnail = None
        # Can be useful when you need to also show the thumbnail of the game.
        # Like in Discord's embeds for example, or anything else.
        # Here I showed it just as example and won't use it.
        for image in game['keyImages']:
            if image['type'] == 'Thumbnail':
                game_thumbnail = image['url']

        game_price = game['price']['totalPrice']['fmtPrice']['originalPrice']
        game_promotions = game['promotions']['promotionalOffers']
        upcoming_promotions = game['promotions']['upcomingPromotionalOffers']
        
        if game_promotions and game['price']['totalPrice']['discountPrice'] == 0:
            # Promotion is active.
            promotion_data = game_promotions[0]['promotionalOffers'][0]
            end_date_iso = (promotion_data['endDate'][:-1])
            # Remove the last "Z" character so Python's datetime can parse it.
            end_date = datetime.fromisoformat(end_date_iso)
            # Create a timezone object for UTC
            utc_timezone = timezone.utc
            # Attach the UTC timezone to the datetime object
            end_date = end_date.replace(tzinfo=utc_timezone)
            # Convert UTC time to PST
            pst_timezone = timezone(timedelta(hours=-8))  # Pacific Standard Time (UTC-8)
            pst_time = end_date.astimezone(pst_timezone)
            # Format the PST time in 12-hour format without seconds
            formatted_pst_time = pst_time.strftime("%Y-%m-%d %I:%M %p")
            cur.append(f'{game_title} ({game_price}) is FREE until {formatted_pst_time} \n {game_url}')
            cur.append(game_thumbnail)
            
        if not game_promotions and upcoming_promotions:
            # Promotion is not active yet, but will be active soon.
            promotion_data = upcoming_promotions[0]['promotionalOffers'][0]
            start_date_iso = (promotion_data['startDate'][:-1])
            # Remove the last "Z" character so Python's datetime can parse it.
            start_date = datetime.fromisoformat(start_date_iso)
            fut.append(start_date.weekday())
            fut.append(start_date.replace(tzinfo=timezone.utc).astimezone(tz=None).time().strftime("%I:%M:%S"))
            # print(f'* {game_title} ({game_price}) will be free from {start_date} UTC \n {game_url}')
            #fut.append(f'* {game_title} ({game_price}) will be free from {start_date} UTC \n {game_url}')
    promos["current"] = cur
    promos["future"] = fut
    return promos

def test():
    curtime = datetime.now() + timedelta(seconds=10)
    scheduled_datetime = curtime.strftime("%H:%M:%S") 
    tday = datetime.today().weekday()
    fut = [tday, scheduled_datetime]
    cur = []
    promos = {}
    promos["current"] = cur
    promos["future"] = fut
    return promos