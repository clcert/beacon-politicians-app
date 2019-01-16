import requests
import datetime
import random
import parser.deputies as pd

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader('diputadodeldia'),
                  autoescape=select_autoescape(['html', 'xml']))


class Generator:

    @staticmethod
    def get_index(seed_value):
        """
        Get a random number in the range of the deputies list length using as seed the value delivered by the beacon.
        :return: An integer in the range of the list described.
        """
        max_index = pd.Parser().count_deputies() - 1
        random.seed(bytes.fromhex(seed_value))

        return random.randint(0, max_index)

    @staticmethod
    def format_date(value):
        if value < 10:
            return '0' + str(value)
        else:
            return str(value)

    def run(self):
        url = 'https://beacon.clcert.cl/beacon/2.0/pulse/last'
        page = requests.get(url)
        output_value = page.json()['pulse']['outputValue']
        record_id = page.json()['pulse']['pulseIndex']
        date = datetime.datetime.strptime(page.json()['pulse']['timeStamp'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
            tzinfo=datetime.timezone.utc)
        yesterday = date - datetime.timedelta(days=1)
        tomorrow = date + datetime.timedelta(days=1)

        index = self.get_index(output_value)

        parser = pd.Parser()
        deputy = parser.get_deputy(index)

        template = env.get_template('index_template.html')
        curr_html_name = str(date.year) + self.format_date(date.month) + self.format_date(date.day) + '.html'
        prev_html_name = str(yesterday.year) + self.format_date(yesterday.month) + self.format_date(
            yesterday.day) + '.html'
        post_html_name = str(tomorrow.year) + self.format_date(tomorrow.month) + self.format_date(
            tomorrow.day) + '.html'

        with open('public/' + curr_html_name, 'w') as html_file:
            html_file.write(template.render(**deputy, date=date, record=record_id, prev=prev_html_name,
                                            post=post_html_name))
            html_file.close()

        with open('public/index.html', 'w') as html_file:
            html_file.write(template.render(**deputy, date=date, record=record_id, prev=prev_html_name,
                                            post='#'))
            html_file.close()


Generator().run()
