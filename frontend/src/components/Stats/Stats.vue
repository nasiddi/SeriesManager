<template>
  <div v-if="json.length !== 0 && 'shows' in json">
    <b-row>
      <b-col lg>
        <b-row class="text-center">
          <b-col class="text-center">
            <h4 class="mt-3">Total</h4>
          </b-col>
          <b-col class="text-center">
            <h4 class="mt-3">Average</h4>
          </b-col>
        </b-row>
        <hr>
        <b-row class="mt-3">
          <b-col class="text-center mt-2">
            <span class="mt-2"><strong>{{
            Math.round(totalHours / 24 * 100) / 100 }}</strong></span><br>
            <span>days</span>
          </b-col>
          <b-col class="text-center mt-2">
            <span class="mt-2"><strong>{{
              (totalEpisodes > 0) ? Math.round(
            totalHours / totalEpisodes * 60 * 100) / 100 : 0 }}</strong></span><br>
            <span>minutes per Episode</span>
          </b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col class="text-center mb-2">
            <span class="mt-2"><strong>{{ totalHours }}</strong></span><br>
            <span>hours</span>
          </b-col>
          <b-col>
            <b-col class="text-center mb-2">
              <span class="mt-2"><strong>{{ (totalShows > 0) ? Math.round(
              totalHours / totalShows * 100) / 100 : 0 }}</strong></span><br>
              <span>hours per Show</span>
            </b-col>
          </b-col>
        </b-row>
        <hr>
        <b-row class="mt-3">
          <b-col class="text-center mt-2">
            <span class="mt-2"><strong>{{ totalShows }}</strong></span><br>
            <span>Shows</span>
          </b-col>
          <b-col>
            <b-col class="text-center mt-2">
              <span class="mt-2"><strong>{{ (totalShows > 0) ? Math.round(
              totalSeasons/ totalShows * 100) / 100 : 0 }}</strong></span><br>
              <span>Seasons per Show</span>
            </b-col>
          </b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col class="text-center">
            <span class="mt-2"><strong>{{ totalSeasons }}</strong></span><br>
            <span>Seasons</span>
          </b-col>
          <b-col>
            <b-col class="text-center">
              <span class="mt-2"><strong>{{ (totalSeasons > 0) ? Math.round(
              totalEpisodes / totalSeasons * 100) / 100 : 0 }}</strong></span><br>
              <span>Episodes per Season</span>
            </b-col>
          </b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col class="text-center mb-2">
            <span class="mt-2"><strong>{{ totalEpisodes }}</strong></span><br>
            <span>Episodes</span>
          </b-col>
          <b-col>
            <b-col class="text-center mb-2">
              <span class="mt-2"><strong>{{ (totalShows > 0) ? Math.round(
              totalEpisodes / totalShows * 100) / 100 : 0 }}</strong></span><br>
              <span>Episodes per Show</span>
            </b-col>
          </b-col>
        </b-row>
        <hr>
        <b-row class="mt-3">
          <b-col class="text-center mt-2">
            <span class="mt-2"><strong>{{ Math.round(
            totalGB / 1024 * 100) / 100 }}</strong></span><br>
            <span>TB</span>
          </b-col>
          <b-col class="text-center mt-2">
            <span class="mt-2"><strong>{{ (totalEpisodes > 0) ? Math.round(
            totalGB * 1024 / totalEpisodes * 100) / 100 : 0 }}</strong></span><br>
            <span>MB per Episode</span>
          </b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col class="text-center">
            <span class="mt-2"><strong>{{ totalGB }}</strong></span><br>
            <span>GB</span>
          </b-col>
          <b-col>
            <b-col class="text-center">
              <span class="mt-2"><strong>{{ (totalShows > 0) ? Math.round(
              totalGB / totalShows * 100) / 100 : 0 }}</strong></span><br>
              <span>GB per Show</span>
            </b-col>
          </b-col>
        </b-row>
      </b-col>
      <b-col>
        <b-row lg>
          <b-col class="text-center">
            <h4 class="mt-3">Status</h4>
            <pie-chart
              :chart-data="getPieData(totalPies('status'))"
              :options="chartOptions"
              :style="{display: 'inline-block'}"
              :width="230"
              :height="230"
            />
          </b-col>
          <b-col
            class="text-center">
            <h4 class="mt-3">Quality</h4>
            <pie-chart
              :chart-data="getPieData(totalPies('quality'))"
              :options="chartOptions"
              :style="{display: 'inline-block'}"
              :width="230"
              :height="230"
            />
          </b-col>
        </b-row>
        <b-row
          lg
          class="mb-5">
          <b-col
            :style="{margin: 'auto', position: 'relative'}"
            class="text-center"
          >
            <h4
              class="mt-3">Extentions</h4>
            <pie-chart
              :chart-data="getPieData(totalPies('extension'))"
              :options="chartOptions"
              :style="{display: 'inline-block'}"
              :width="230"
              :height="230"
            />
          </b-col>
          <b-col
            class="text-center"
          >
            <h4 class="mt-3">Aspect Ratio</h4>
            <pie-chart
              :chart-data="getPieData(totalPies('ratio'))"
              :options="chartOptions"
              :style="{display: 'inline-block'}"
              :width="230"
              :height="230"
            />
          </b-col>
        </b-row>
      </b-col>
    </b-row>
    <div>
      <b-card>
        <b-row class="mt-3">
          <b-col>
            <b-button
              :pressed.sync="cards"
              :variant="'outline-primary'"
              :style="{width: '100%'}"
            >Cards</b-button>
          </b-col>
          <b-col>
            <b-button
              :variant="'outline-primary'"
              :style="{width: '100%'}"
              :pressed.sync="table"
            >Table</b-button>
          </b-col>
        </b-row>
        <div>
          <hr>
          <b-row>
            <b-col>
              <b-button
                :pressed.sync="additive"
                :variant="'outline-primary'"
                :style="{width: '100%'}"
              >{{ (additive) ? 'Additive' : 'Subtractive' }}
              </b-button>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col class="mx-3">
              <b-row>
                <b-form-checkbox-group
                  v-model="selected"
                  :options="['Airing', 'Hiatus', 'Ended']"
                  :style="{width: '100%'}"
                  stacked
                  buttons
                  button-variant="outline-secondary"
                  name="status"/>
              </b-row>
              <b-row class="mt-4">
                <b-form-checkbox-group
                  v-model="selected"
                  :options="['SD', 'HD', 'FullHD']"
                  :style="{width: '100%'}"
                  stacked
                  buttons
                  button-variant="outline-secondary"
                  name="quality"/>
              </b-row>
              <b-row class="my-4">
                <b-form-checkbox-group
                  v-model="selected"
                  :options="json.ratio"
                  :style="{width: '100%'}"
                  stacked
                  buttons
                  button-variant="outline-secondary"
                  name="ratio"/>
              </b-row>
            </b-col>
            <b-col class="mx-3">
              <b-row>
                <b-form-checkbox-group
                  v-model="selected"
                  :options="json.extension"
                  :style="{width: '100%'}"
                  stacked
                  buttons
                  button-variant="outline-secondary"
                  name="extension"/>
              </b-row>
              <b-row class="my-4">
                <b-form-checkbox-group
                  v-model="selected"
                  :options="['Premiere', 'Final']"
                  :style="{width: '100%'}"
                  stacked
                  buttons
                  button-variant="outline-secondary"
                  name="extension"/>
              </b-row>
            </b-col>
            <b-col class="mx-3">
              <b-row>
                <b-form-checkbox-group
                  v-model="selected"
                  :options="genres"
                  :style="{width: '100%'}"
                  stacked
                  buttons
                  button-variant="outline-secondary"
                  name="genres"/>
              </b-row>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col>
              <b-button
                :style="{width: '100%'}"
                variant="primary"
                class="mt-2"
                @click="selectAllFilters"
              >Select All</b-button>
            </b-col>
            <b-col>
              <b-button
                :style="{width: '100%'}"
                variant="primary"
                class="mt-2"
                @click="selected = []"
              >Select None</b-button>
            </b-col>
          </b-row>
          <hr>
          <b-row md>
            <b-col md>
              <b-row>
                <b-col class="text-center">
                  <span><strong>Premiere</strong></span>
                </b-col>
              </b-row>
              <b-row sm>
                <b-col sm>
                  <b-input
                    v-model="premiereStart"
                    :formatter="dateFormat"
                    class="mt-2"
                    lazy-formatter
                    placeholder="Premiere Start"/>
                </b-col>
                <b-col sm>
                  <b-form-input
                    v-model="premiereEnd"
                    :formatter="dateFormat"
                    type="text"
                    class="mt-2"
                    lazy-formatter
                    placeholder="Premiere End"/>
                </b-col>
              </b-row>
            </b-col>
            <b-col md>
              <b-row>
                <b-col class="text-center">
                  <span><strong>Final</strong></span>
                </b-col>
              </b-row>
              <b-row sm>
                <b-col sm>
                  <b-input
                    v-model="finalStart"
                    :formatter="dateFormat"
                    class="mt-2"
                    lazy-formatter
                    placeholder="Final Start"/>
                </b-col>
                <b-col sm>
                  <b-form-input
                    v-model="finalEnd"
                    :formatter="dateFormat"
                    type="text"
                    class="mt-2"
                    lazy-formatter
                    placeholder="Final End"/>
                </b-col>
              </b-row>
            </b-col>
          </b-row>
          <hr>
          <b-row>
            <b-col
              sm="10"
              class="mt-3">
              <b-form-select
                v-model="sorter"
                :options="sortOptions"
                :style="{width: '100%'}"
                selected="Series"/>
            </b-col>
            <b-col class="mt-3">
              <b-button
                :variant="'primary'"
                :style="{width: '100%'}"
                @click.prevent="changeDirection"
              ><font-awesome-icon :icon="direction"/></b-button>
            </b-col>
          </b-row>
        </div>
      </b-card>
      <div v-if="cards">
        <stats-card
          v-for="show in shows"
          :key="show.series_name"
          :show="show"
          class="mt-3"/>
      </div>
      <div v-if="table">
        <b-table
          :items="getTable"
          :fields="fields"
          class="mt-3"/>
      </div>
    </div>
  </div>
</template>

<script>
import PieChart from '@/components/Snippets/PieChart';
import StatsCard from './StatsCard';


const _ = require('lodash');


export default {
  components: {
    PieChart,
    StatsCard,
  },
  data: () => ({
    sorter: 'series_name',
    sortOptions: [
      { value: 'series_name', text: 'Series Name' },
      { value: 'seasons', text: 'Number of Seasons' },
      { value: 'episodes', text: 'Number of Episodes' },
      { value: 'premiere', text: 'Premiere' },
      { value: 'final', text: 'Final' },
      { value: 'duration', text: 'Duration' },
      { value: 'avg_duration', text: 'Average Duration' },
      { value: 'size', text: 'Size' },
      { value: 'avg_size', text: 'Average Size' },
    ],
    fields: [
      {
        key: 'series_name',
        sortable: true,
      },
      {
        key: 'status',
        sortable: true,
      },
      {
        key: '\u0023S',
        sortable: true,
      },
      {
        key: '\u0023E',
        sortable: true,
      },
      {
        key: 'hours',
        sortable: true,
      },
      {
        key: 'minutes_per_Episode',
        sortable: true,
      },
      {
        key: 'GB',
        sortable: true,
      },
      {
        key: 'MB_per_Episode',
        sortable: true,
      },
      {
        key: 'premiere',
        sortable: true,
      },
      {
        key: 'final',
        sortable: true,
      },
    ],
    table: false,
    cards: true,
    direction: 'sort-down',
    selected: [],
    json: {},
    chartOptions: {
      legend: {
        display: true,
      },
      responsive: false,
    },
    shows: [],
    primaryExt: [],
    sencondaryExt: [],
    additive: true,
    genres: [],
    premiereStart: '',
    premiereEnd: '',
    finalStart: '',
    finalEnd: '',
  }),
  computed: {
    getTable() {
      const table = [];
      this.shows.forEach((s) => {
        table.push({
          series_name: s.series_name,
          status: _.keys(s.status)[0],
          '\u0023S': s.seasons,
          '\u0023E': s.episodes,
          hours: s.duration,
          minutes_per_Episode: s.avg_duration,
          GB: s.size,
          MB_per_Episode: s.avg_size,
          premiere: s.premiere,
          final: s.final,
        });
      });
      return table;
    },
    totalHours() {
      return Math.round(_.sumBy(this.shows, 'duration') * 100) / 100;
    },
    totalEpisodes() {
      return _.sumBy(this.shows, 'episodes');
    },
    totalSeasons() {
      return _.sumBy(this.shows, 'seasons');
    },
    totalShows() {
      return this.shows.length;
    },
    totalGB() {
      return Math.round(_.sumBy(this.shows, 'size') * 100) / 100;
    },
    averageDuration() {
      const durations = {
        25: 0, 45: 0, 60: 0, 90: 0,
      };

      this.shows.forEach((s) => {
        const x = s.avg_duration;
        const closest = _.keys(durations).sort((a, b) => Math.abs(x - a) - Math.abs(x - b))[0];
        durations[closest] += 1;
      });
      return durations;
    },
    genreSum() {
      const genres = _.zipObject(_.map(this.genres, 'text'), [0] * this.genres.length);
      genres[''] = 0;
      this.shows.forEach((s) => {
        genres[s.genre1] += 1;
        genres[s.genre2] += 1;
      });
      return genres;
    },
  },
  watch: {
    selected: {
      handler() {
        this.applyFilterAndSorter();
      },
      deep: true,
    },
    premiereStart: {
      handler() {
        this.applyFilterAndSorter();
      },
      deep: true,
    },
    premiereEnd: {
      handler() {
        this.applyFilterAndSorter();
      },
      deep: true,
    },
    finalStart: {
      handler() {
        this.applyFilterAndSorter();
      },
      deep: true,
    },
    finalEnd: {
      handler() {
        this.applyFilterAndSorter();
      },
      deep: true,
    },
    sorter: {
      handler() {
        this.applyFilterAndSorter();
      },
      deep: true,
    },
    additive: {
      handler() {
        this.applyFilterAndSorter();
      },
      deep: true,
    },
    cards: {
      handler() {
        if (this.cards) {
          this.table = false;
        } else {
          this.table = true;
        }
      },
    },
    table: {
      handler() {
        if (this.table) {
          this.cards = false;
        } else {
          this.cards = true;
        }
      },
    },
    direction: {
      handler() {
        this.applyFilterAndSorter();
      },
      deep: true,
    },
  },
  created() {
    this.getGenres().forEach((g) => {
      if (g === '') {
        this.genres.push({ value: g, text: 'None' });
      } else {
        this.genres.push({ value: g, text: g });
      }
    });
    this.resetDates();
    this.loadData();
  },
  methods: {
    resetDates() {
      const currentDate = new Date().toISOString().slice(0, 10);
      this.premiereEnd = currentDate;
      this.finalEnd = currentDate;
      this.premiereStart = '1960-01-01';
      this.finalStart = '1960-01-01';
    },
    dateFormat(value) {
      if (value.length === 4) {
        const year = parseInt(value, 10);
        // eslint-disable-next-line no-restricted-globals
        if (!isNaN(year)) {
          // eslint-disable-next-line no-param-reassign
          value = `${value}-01-01`;
        }
      }
      if (this.isValidDateWithDash(value)) {
        return value;
      }
      return this.isValidDateNoDash(value);
    },
    totalPies(key) {
      let obj = {};
      this.shows.forEach((s) => {
        _.mergeWith(obj, s[key], _.add);
      });
      if (_.size(obj) > 4) {
        const total = _.sum(_.values(obj));
        if (total === 0) {
          return obj;
        }
        let other = 0;
        const keysToDelete = [];
        _.forOwn(obj, (value, k) => {
          if (value / total < 0.05) {
            other += value;
            keysToDelete.push(k);
          }
          obj = _.omit(obj, keysToDelete);
          obj.other = other;
        });
      }
      return obj;
    },
    unlockShows() {
      this.$snotify.remove(this.notifLock.id);
      this.$http.post('python/unlock')
        .then(
          (res) => {
            this.json = res;
            this.loadData();
          },
        );
    },
    loadData() {
      this.notifLoading = this.$snotify.info('Loading', { timeout: 0 });
      this.$http
        .post('python/stats')
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            if (res.body === 'failed') {
              this.$snotify.remove(this.notifLoading.id);
              this.$snotify.error('Python failed', { timeout: 0 });
              return;
            }
            if ('shows_locked' in body) {
              this.notifLock = this.$snotify.confirm('', 'Shows locked', {
                timeout: 0,
                buttons: [
                  { text: 'Unlock', action: () => this.unlockShows(), bold: true },
                ],
              });
            } else {
              this.json = body;
              this.shows = body.shows;
              this.selectAllFilters();
            }
            this.$snotify.remove(this.notifLoading.id);
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
    },
    switchView() {
      if (this.cards) {
        this.cards = false;
      }
    },
    applyFilterAndSorter() {
      if (!('shows' in this.json)) { return; }
      let series = [];
      if (this.additive) {
        series = series.concat(this.filterGroup(this.json.status, 'status', this.json.shows));
        series = series.concat(this.filterGroup(this.json.ratio, 'ratio', this.json.shows));
        series = series.concat(this.filterGroup(this.json.extension, 'extension', this.json.shows));
        series = series.concat(this.filterGroup(this.json.quality, 'quality', this.json.shows));
        series = series.concat(this.filterGenre(this.json.shows));
        series = series.concat(this.filterDates(this.json.shows, 'premiere'));
        series = series.concat(this.filterDates(this.json.shows, 'final'));
      } else {
        series = this.filterGroup(this.json.status, 'status', this.json.shows);
        series = this.filterGroup(this.json.ratio, 'ratio', series);
        series = this.filterGroup(this.json.extension, 'extension', series);
        series = this.filterGroup(this.json.quality, 'quality', series);
        series = this.filterGenre(series);
        series = this.filterDates(series, 'premiere');
        series = this.filterDates(series, 'final');
      }
      series = [...new Set(series.map(s => s.series_name))];
      const temp = [];
      this.json.shows.forEach((s) => {
        if (series.includes(s.series_name)) {
          temp.push(s);
        }
      });
      this.shows = temp;
      let dir;
      if (this.direction === 'sort-up') {
        dir = -1;
      } else {
        dir = 1;
      }
      this.shows.sort(this.dynamicSort(this.sorter, dir));
    },
    filterDates(series, key) {
      let start = null;
      let end = null;
      if (!this.selected.includes(key[0].toUpperCase() + key.slice(1))) {
        if (this.additive) {
          return [];
        }
        return series;
      }
      if (key === 'premiere') {
        start = (this.premiereStart) ? new Date(this.premiereStart) : '1960-10-01';
        end = (this.premiereEnd) ? new Date(this.premiereEnd)
          : new Date().toISOString().slice(0, 10);
      } else {
        start = (this.finalStart) ? new Date(this.finalStart) : '1960-10-01';
        end = (this.finalEnd) ? new Date(this.finalEnd) : new Date().toISOString().slice(0, 10);
      }
      const shows = [];
      series.forEach((s) => {
        const date = new Date(s[key]);
        if (start.getTime() <= date.getTime() && date.getTime() <= end.getTime()) {
          shows.push(s);
        }
      });
      return shows;
    },
    filterGroup(group, name, series) {
      const filteredGroup = [];
      const shows = [];
      group.forEach((g) => {
        if (this.selected.includes(g)) {
          filteredGroup.push(g);
        }
      });
      series.forEach((s) => {
        if (_.keys(s[name]).some(n => filteredGroup.indexOf(n) >= 0)) {
          shows.push(s);
        }
      });
      return shows;
    },
    filterGenre(series) {
      const filteredGroup = [];
      const shows = [];
      this.getGenres().forEach((g) => {
        if (this.selected.includes(g)) {
          filteredGroup.push(g);
        }
      });
      series.forEach((s) => {
        if (filteredGroup.includes(s.genre1) || filteredGroup.includes(s.genre2)) {
          shows.push(s);
        }
      });
      return shows;
    },
    changeDirection() {
      if (this.direction === 'sort-down') {
        this.direction = 'sort-up';
      } else {
        this.direction = 'sort-down';
      }
    },
    selectAllFilters() {
      this.selected = [];
      this.selected = this.json.extension;
      this.selected = this.selected.concat(this.json.status);
      this.selected = this.selected.concat(this.json.ratio);
      this.selected = this.selected.concat(this.json.quality);
      this.selected = this.selected.concat(this.getGenres());
      this.selected = this.selected.concat(['Premiere', 'Final']);
      this.resetDates();
    },
    getPieData(pie) {
      const data = { labels: [], datasets: [{ data: [], backgroundColor: [] }] };
      data.labels = _.keys(pie);
      data.datasets[0].data = _.values(pie);
      data.datasets[0].backgroundColor = this.colorArrayRandom(
        _.keys(pie),
      );
      return data;
    },
    dynamicSort(property, sortOrder) {
      // eslint-disable-next-line func-names
      return function (a, b) {
        const aProp = a[property];
        const bProp = b[property];
        if (typeof aProp === 'string') {
          aProp.toLowerCase();
          bProp.toLowerCase();
        }
        // eslint-disable-next-line no-nested-ternary
        const result = (aProp < bProp) ? -1
          : (aProp > bProp) ? 1 : 0;
        return result * sortOrder;
      };
    },
  },
};
</script>
