<template>
  <div>
    <b-row v-if="json.length !== 0 && 'total' in json">
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
            <span class="mt-2"><strong>{{ json.total.days }}</strong></span><br>
            <span>days</span>
          </b-col>
          <b-col class="text-center mt-2">
            <span class="mt-2"><strong>{{ json.total.avg_duration_ep }}</strong></span><br>
            <span>minutes per Episode</span>
          </b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col class="text-center mb-2">
            <span class="mt-2"><strong>{{ json.total.hours }}</strong></span><br>
            <span>hours</span>
          </b-col>
          <b-col>
            <b-col class="text-center mb-2">
              <span class="mt-2"><strong>{{ json.total.avg_duration_show }}</strong></span><br>
              <span>hours per Show</span>
            </b-col>
          </b-col>
        </b-row>
        <hr>
        <b-row class="mt-3">
          <b-col class="text-center mt-2">
            <span class="mt-2"><strong>{{ json.total.shows }}</strong></span><br>
            <span>Shows</span>
          </b-col>
          <b-col>
            <b-col class="text-center mt-2">
              <span class="mt-2"><strong>{{ json.total.avg_sea_show }}</strong></span><br>
              <span>Seasons per Show</span>
            </b-col>
          </b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col class="text-center">
            <span class="mt-2"><strong>{{ json.total.seas }}</strong></span><br>
            <span>Seasons</span>
          </b-col>
          <b-col>
            <b-col class="text-center">
              <span class="mt-2"><strong>{{ json.total.avg_ep_sea }}</strong></span><br>
              <span>Episodes per Season</span>
            </b-col>
          </b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col class="text-center mb-2">
            <span class="mt-2"><strong>{{ json.total.eps }}</strong></span><br>
            <span>Episodes</span>
          </b-col>
          <b-col>
            <b-col class="text-center mb-2">
              <span class="mt-2"><strong>{{ json.total.avg_ep_show }}</strong></span><br>
              <span>Episodes per Show</span>
            </b-col>
          </b-col>
        </b-row>
        <hr>
        <b-row class="mt-3">
          <b-col class="text-center mt-2">
            <span class="mt-2"><strong>{{ json.total.tb }}</strong></span><br>
            <span>TB</span>
          </b-col>
          <b-col class="text-center mt-2">
            <span class="mt-2"><strong>{{ json.total.avg_mb_ep }}</strong></span><br>
            <span>MB per Episode</span>
          </b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col class="text-center">
            <span class="mt-2"><strong>{{ json.total.gb }}</strong></span><br>
            <span>GB</span>
          </b-col>
          <b-col>
            <b-col class="text-center">
              <span class="mt-2"><strong>{{ json.total.avg_gb_show }}</strong></span><br>
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
              :chart-data="getPieData(json.total.status)"
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
              :chart-data="getPieData(json.total.quality)"
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
              :chart-data="getPieData(json.total.extention)"
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
              :chart-data="getPieData(json.total.ratio)"
              :options="chartOptions"
              :style="{display: 'inline-block'}"
              :width="230"
              :height="230"
            />
          </b-col>
        </b-row>
      </b-col>
    </b-row>
    <div v-if="json.length !== 0 && 'shows' in json">
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
        <div v-if="cards">
          <hr>
          <b-row>
            <b-col v-if="json.length !== 0 && 'total' in json">
              <b-form-checkbox-group
                v-model="selected"
                :options="_.keys(json.total.status)"
                :style="{width: '100%'}"
                stacked
                buttons
                button-variant="outline-primary"
                name="status"/>
            </b-col>
            <b-col>
              <b-form-checkbox-group
                v-model="selected"
                :options="_.keys(json.total.quality)"
                :style="{width: '100%'}"
                stacked
                buttons
                button-variant="outline-primary"
                name="quality"/>
            </b-col>
            <b-col>
              <b-form-checkbox-group
                v-model="selected"
                :options="_.keys(json.total.ratio)"
                :style="{width: '100%'}"
                stacked
                buttons
                button-variant="outline-primary"
                name="ratio"/>
            </b-col>
            <b-col>
              <b-form-checkbox-group
                v-model="selected"
                :options="setExtentions(true)"
                :style="{width: '100%'}"
                stacked
                buttons
                button-variant="outline-primary"
                name="extention"/>
            </b-col>
            <b-col>
              <b-form-checkbox-group
                v-model="selected"
                :options="setExtentions(false)"
                :style="{width: '100%'}"
                stacked
                buttons
                button-variant="outline-primary"
                name="extention"/>
            </b-col>
          </b-row>
          <b-row class="mt-3">
            <b-col>
              <b-button
                :pressed.sync="all"
                :variant="'outline-primary'"
                :style="{width: '100%'}"
                @click.prevent="selectAllFilters"
              >Select All</b-button>
            </b-col>
          </b-row>
          <hr>
          <b-row class="mt-3">
            <b-col sm="10">
              <b-form-select
                v-model="sorter"
                :options="sortOptions"
                :style="{width: '100%'}"
                selected="Series"/>
            </b-col>
            <b-col>
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
import StatsCard from '@/components/StatsCard';


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
        key: 'Final',
        sortable: true,
      },
    ],
    table: false,
    cards: true,
    all: true,
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
  },
  watch: {
    selected: {
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
    this.notifLoading = this.$snotify.info('Loading', {
      timeout: 0,
    });
    this.$http
      .post('jobs/stats')
      .then(
        (res) => {
          const body = _.defaults(res.body, {
          });
          this.json = body;
          this.shows = body.shows;
          this.selectAllFilters();

          this.$snotify.remove(this.notifLoading.id);
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
  },
  methods: {
    switchView() {
      if (this.cards) {
        this.cards = false;
      }
    },
    applyFilterAndSorter() {
      if (!('total' in this.json)) { return; }
      let series = [];
      this.shows = [];
      series = series.concat(this.filterGroup(_.keys(this.json.total.status), 'status'));
      series = series.concat(this.filterGroup(_.keys(this.json.total.ratio), 'ratio'));
      series = series.concat(this.filterGroup(this.json.extentions, 'extention'));
      series = series.concat(this.filterGroup(_.keys(this.json.total.quality), 'quality'));


      this.json.shows.forEach((s) => {
        if (series.includes(s.series_name)) {
          this.shows.push(s);
        }
      });
      let dir;
      if (this.direction === 'sort-up') {
        dir = -1;
      } else {
        dir = 1;
      }
      this.shows.sort(this.dynamicSort(this.sorter, dir));
    },
    filterGroup(group, name) {
      const filteredGroup = [];
      const shows = [];
      group.forEach((g) => {
        if (this.selected.includes(g)) {
          filteredGroup.push(g);
        }
      });

      this.json.shows.forEach((s) => {
        if (_.keys(s[name]).some(n => filteredGroup.indexOf(n) >= 0)) {
          shows.push(s.series_name);
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
      if (this.all) {
        this.selected = this.json.extentions;
        this.selected = this.selected.concat(_.keys(this.json.total.status));
        this.selected = this.selected.concat(_.keys(this.json.total.ratio));
        this.selected = this.selected.concat(_.keys(this.json.total.quality));
      }
    },
    setExtentions(primary) {
      if (!('total' in this.json)) {
        return [];
      }
      const ext = [];
      this.json.extentions.forEach((e) => {
        if (primary && e in this.json.total.extention) {
          ext.push(e);
        } else if (!primary && !(e in this.json.total.extention)) { ext.push(e); }
      });
      return ext;
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
