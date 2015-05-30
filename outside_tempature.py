# -*- coding: utf-8 -*-
"""
Display Yahoo! Weather forecast as icons.

Based on Yahoo! Weather. forecast, thanks guys !
    http://developer.yahoo.com/weather/

Find your city code using:
    http://answers.yahoo.com/question/index?qid=20091216132708AAf7o0g

Configuration parameters:
    - cache_timeout : how often to check for new forecasts
    - city_code : city code to use
    - forecast_days : how many forecast days you want shown
    - request_timeout : check timeout

The city_code in this example is for Paris, France => FRXX0076
"""

from time import time
import requests


class Py3status:

    # available configuration parameters
    cache_timeout = 1800
    city_code = 'FRXX0076'
    forecast_days = 1 
    request_timeout = 10

    def _get_temp(self):
        """
        Ask Yahoo! Weather. for a forecast
        """
        q = requests.get(
            'http://query.yahooapis.com/v1/public/yql?q=' +
            'select item from weather.forecast ' +
            'where location="%s"&format=json' % self.city_code,
            timeout=self.request_timeout
        )

        r = q.json()
        status = q.status_code
        forecasts = []

        if status == 200:

            tempature = r['query']['results']['channel']['item']['condition']['temp']
        else:
            raise Exception('got status {}'.format(status))

        # return current today + forecast_days days forecast
        return "it's "+tempature+"f out!"



    def outside_tempature(self, i3s_output_list, i3s_config):
        """
        This method gets executed by py3status
        """

        response = {
            'cached_until': time() + self.cache_timeout,
            'color':'#00ebff',
            'full_text': ''
        }

        tempature = self._get_temp()

        response['full_text'] += '{} '.format(tempature)
        response['full_text'] = response['full_text'].strip()

        return response

if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_good': '#00FF00',
        'color_bad': '#FF0000',
    }
    while True:
        print(x.outside_tempature([], config))
        sleep(1)
