import os
import gzip
import shutil
import json
import datetime
from datetime import date
from textblob import TextBlob


gFilename = ""
gFilepathZipped = "F:\\zipped"
gFilepathUnzipped = "F:\\unzipped"
gFilepathCleaned = "F:\\cleaned"
gLines = 50000
gSelectedCols = [
    # Money
    '/data/goal', '/data/currency', '/data/country', '/data/usd_pledged',
    # Categories
    '/data/category/slug',
    # Dates
    '/data/deadline', '/data/created_at', '/data/launched_at',
    # Text sentiment
    '/data/name', '/data/blurb',
    # Classification
    '/data/state'
]

# 0 : empirical data
# 1 : text data (will run sentiment analysis on)
# 2 : reference data (links/urls)
# 3 : date (requires further analysis)
keys = {
    '/table_id': 0,
    '/robot_id': 0,
    '/run_id': 0,
    '/data/id': 0,
    '/data/photo/key': 0,
    '/data/photo/full': 2,
    '/data/photo/ed': 2,
    '/data/photo/med': 2,
    '/data/photo/little': 2,
    '/data/photo/small': 2,
    '/data/photo/thumb': 2,
    '/data/photo/1024x576': 2,
    '/data/photo/1536x864': 2,
    '/data/name': 1,
    '/data/blurb': 1,
    '/data/goal': 0,
    '/data/pledged': 0,
    '/data/state': 0,
    '/data/slug': 0,
    '/data/disable_communication': 0,
    '/data/country': 0,
    '/data/currency': 0,
    '/data/currency_symbol': 0,
    '/data/currency_trailing_code': 0,
    '/data/deadline': 3,
    '/data/state_changed_at': 3,
    '/data/created_at': 3,
    '/data/launched_at': 3,
    '/data/staff_pick': 0,
    '/data/is_starrable': 0,
    '/data/backers_count': 0,
    '/data/static_usd_rate': 0,
    '/data/usd_pledged': 0,
    '/data/converted_pledged_amount': 0,
    '/data/fx_rate': 0,
    '/data/current_currency': 0,
    '/data/usd_type': 0,
    '/data/creator/id': 0,
    '/data/creator/name': 0,
    '/data/creator/slug': 0,
    '/data/creator/is_registered': 0,
    '/data/creator/chosen_currency': 0,
    '/data/creator/avatar/thumb': 2,
    '/data/creator/avatar/small': 2,
    '/data/creator/avatar/medium': 2,
    '/data/creator/urls/web/user': 0,
    '/data/creator/urls/api/user': 0,
    '/data/location/id': 0,
    '/data/location/name': 0,
    '/data/location/slug': 0,
    '/data/location/short_name': 0,
    '/data/location/displayable_name': 0,
    '/data/location/localized_name': 0,
    '/data/location/country': 0,
    '/data/location/state': 0,
    '/data/location/type': 0,
    '/data/location/is_root': 0,
    '/data/location/urls/web/discover': 0,
    '/data/location/urls/web/location': 0,
    '/data/location/urls/api/nearby_projects': 0,
    '/data/category/id': 0,
    '/data/category/name': 0,
    '/data/category/slug': 0,
    '/data/category/position': 0,
    '/data/category/parent_id': 0,
    '/data/category/color': 0,
    '/data/category/urls/web/discover': 0,
    '/data/profile/id': 0,
    '/data/profile/project_id': 0,
    '/data/profile/state': 0,
    '/data/profile/state_changed_at': 3,
    '/data/profile/name': 1,
    '/data/profile/blurb': 1,
    '/data/profile/background_color': 0,
    '/data/profile/text_color': 0,
    '/data/profile/link_background_color': 0,
    '/data/profile/link_text_color': 0,
    '/data/profile/link_text': 0,
    '/data/profile/link_url': 0,
    '/data/profile/show_feature_image': 0,
    '/data/profile/background_image_opacity': 0,
    '/data/profile/should_show_feature_image_section': 0,
    '/data/profile/feature_image_attributes/image_urls/default': 2,
    '/data/profile/feature_image_attributes/image_urls/baseball_card': 2,
    '/data/spotlight': 0,
    '/data/urls/web/project': 0,
    '/data/urls/web/rewards': 0,
    '/data/source_url': 2
}


def get_data_by_line(filename, lines):
    data = []
    count = 1
    with open(filename, 'rb') as f:
        for line in f:
            data.append(json.loads(line))
            if lines == 0 or int(lines) == 0:
                count = count + 1
                continue
            if count == int(lines):
                break
            else:
                count = count + 1
    return data


def get_cols(dictionary, parent, search, flag):
    retval = ''
    for key, value in dictionary.items():
        if isinstance(value, dict):
            retval = retval + get_cols(value, parent + '/' + key, search, flag)
            continue
        if parent + '/' + key == search:
            if flag == 0:
                if value is not str:
                    retval = retval + str(value)
                else:
                    retval = retval + value
            elif flag == 1:
                sent = TextBlob(value).sentiment
                retval = retval + str(sent.polarity) + "\"" + "," + "\"" + str(sent.subjectivity)
            elif flag == 2:
                pass
            elif flag == 3:
                # get_season(datetime.datetime.fromtimestamp(value))
                if value is not str:
                    retval = retval + str(value)
                else:
                    retval = retval + value
    return retval


Y = 2000  # dummy leap year to allow input X-02-29 (leap day)
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]


def get_season(now):
    if isinstance(now, datetime.datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)


def parse():
    data = get_data_by_line(gFilepathUnzipped + "\\" + gFilename, gLines)
    header_output = ""
    cleaned_line = ""
    cleaned_output = ""
    count = 0.0
    deadline = ""
    launched_at = ""
    if len(gSelectedCols) == 0:
        for col, val in keys.iteritems():
            if val == 1:
                header_output = header_output + "\"" + col + "_polarity" + "\"" + ","
                header_output = header_output + "\"" + col + "_subjectivity" + "\"" + ","
            elif col == "/data/launched_at":
                header_output = header_output + "\"" + col + "\"" + "," + "\"" + "duration" + "\"" + ","
            else:
                header_output = header_output + "\"" + col + "\"" + ","
        header_output = header_output[:-1]
        for datum in data:
            cleaned_line = ""
            for col, val in keys.iteritems():
                r = get_cols(datum, '', col, val)
                if col == "/data/deadline":
                    deadline = r
                    r = get_season(datetime.datetime.fromtimestamp(int(r)))
                elif col == "/data/launched_at":
                    launched_at = r
                    r = get_season(datetime.datetime.fromtimestamp(int(r))) \
                        + "\"" + "," + "\"" + str(int(deadline) - int(launched_at))
                elif col == "/data/created_at":
                    r = get_season(datetime.datetime.fromtimestamp(int(r)))
                if r is None:
                    r = "<Not found>"
                cleaned_line = cleaned_line + "\"" + r + "\"" + ","
            if cleaned_line.endswith("\"successful\",") or cleaned_line.endswith("\"failed\","):
                cleaned_output = cleaned_output + cleaned_line[:-1] + "\n"
            count = count + 1.0
            os.system('cls')
            print(str(count / float(gLines) * 100) + "%")
    else:
        for col in gSelectedCols:
            if keys.get(col) == 1:
                header_output = header_output + "\"" + col + "_polarity" + "\"" + ","
                header_output = header_output + "\"" + col + "_subjectivity" + "\"" + ","
            elif col == "/data/launched_at":
                header_output = header_output + "\"" + col + "\"" + "," + "\"" + "duration_sec" + "\"" + ","
            else:
                header_output = header_output + "\"" + col + "\"" + ","
        header_output = header_output[:-1]
        for datum in data:
            cleaned_line = ""
            for col in gSelectedCols:
                r = get_cols(datum, '', col, keys.get(col))
                if col == "/data/deadline":
                    deadline = r
                    print(deadline)
                    r = get_season(datetime.datetime.fromtimestamp(int(r)))
                elif col == "/data/launched_at":
                    launched_at = r
                    print("\t" + launched_at)
                    r = get_season(datetime.datetime.fromtimestamp(int(r))) \
                        + "\"" + "," + "\"" + str(int(deadline) - int(launched_at))
                elif col == "/data/created_at":
                    r = get_season(datetime.datetime.fromtimestamp(int(r)))
                if r is None:
                    r = "<Not found>"
                cleaned_line = cleaned_line + "\"" + r + "\"" + ","
            if cleaned_line.endswith("\"successful\",") or cleaned_line.endswith("\"failed\","):
                cleaned_output = cleaned_output + cleaned_line[:-1] + "\n"
            count = count + 1.0
            os.system('cls')
            print(str(count / float(gLines) * 100) + "%")
    with open(gFilepathCleaned + "\\" + gFilename[:-5] + ".csv", 'w') as output_file:
        output_file.write(header_output + "\n")
        output_file.write(cleaned_output)


def parse_each():
    global gFilename
    f = []
    for (dirpath, dirnames, filenames) in os.walk(gFilepathZipped):
        f.extend(filenames)
        break
    for file in f:
        print("Extracting " + gFilepathZipped + "\\" + file)
        with gzip.open(gFilepathZipped + "\\" + file, 'rb') as gz_file:
            with open(gFilepathUnzipped + "\\" + file[:-3], 'wb') as json_file:
                shutil.copyfileobj(gz_file, json_file)
        gFilename = file[:-3]
        print("gFilename is now " + gFilename)
        parse()
        try:
            os.remove(gFilepathUnzipped + "\\" + gFilename)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))


if __name__ == "__main__":
    parse_each()
