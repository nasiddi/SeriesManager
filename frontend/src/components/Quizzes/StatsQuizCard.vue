<template>
  <div>
    <b-card
      :sub-title="_.keys(show.status)[0]"
      :header-bg-variant="show.color"
      header-tag="header"
      class="text-center">
      <div
        slot="header"
        class="mb-0">
        <b-row>
          <b-col>
            <b-form-select
              v-model="show.selected"
              :options="selector"
              :disabled="show.result"
              class=""
              @change="setColor" />
          </b-col>
          <b-col
            v-if="show.result"
            class="pt-2">
            <h5>{{ show.series_name }}</h5>
          </b-col>
        </b-row>
      </div>
      <b-row
        lg
        class="mt-3">
        <b-col class="text-center mt-2">
          <span class="mt-2"><strong>{{ show.premiere }}</strong></span><br>
          <span>Premiere</span>
        </b-col>
        <b-col class="text-center mt-2">
          <span class="mt-2"><strong>{{ show.final }}</strong></span><br>
          <span>Final</span>
        </b-col>
        <b-col class="text-center mt-2">
          <span class="mt-2"><strong>{{ show.seasons }}</strong></span><br>
          <span>Seasons</span>
        </b-col>
        <b-col class="text-center mt-2">
          <span class="mt-2"><strong>{{ show.episodes }}</strong></span><br>
          <span>Episodes</span>
        </b-col>
      </b-row>
      <hr>
      <b-row
        lg
        class="mt-3">
        <b-col class="text-center mt-2">
          <span class="mt-2"><strong>{{ show.duration }}</strong></span><br>
          <span>Hours</span>
        </b-col>
        <b-col class="text-center mt-2">
          <span class="mt-2"><strong>{{ show.size }}</strong></span><br>
          <span>GB</span>
        </b-col>
        <b-col class="text-center mt-2">
          <span class="mt-2"><strong>{{ show.avg_duration }}</strong></span><br>
          <span>Minutes per Episode</span>
        </b-col>
        <b-col class="text-center mt-2">
          <span class="mt-2"><strong>{{ show.avg_size }}</strong></span><br>
          <span>MB per Episode</span>
        </b-col>
      </b-row>
      <hr>
      <b-row lg>
        <b-col class="text-center">
          <h6 class="mt-3">Extentions</h6>
          <pie-chart
            :chart-data="getPieData(show.extension)"
            :options="chartOptions"
            :style="{display: 'inline-block'}"
            :width="50"
            :height="50"
          />
        </b-col>
        <b-col
          class="text-center">
          <h6 class="mt-3">Quality</h6>
          <pie-chart
            :chart-data="getPieData(show.quality)"
            :options="chartOptions"
            :style="{display: 'inline-block'}"
            :width="50"
            :height="50"
          />
        </b-col>
        <b-col
          class="text-center">
          <h6 class="mt-3">Aspect Ratio</h6>
          <pie-chart
            :chart-data="getPieData(show.ratio)"
            :options="chartOptions"
            :style="{display: 'inline-block'}"

            :width="50"
            :height="50"
          />
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>
import PieChart from '@/components/Snippets/PieChart';

const _ = require('lodash');


export default {
  components: {
    PieChart,
  },
  props: {
    show: {
      type: Object,
      required: true,
    },
    selector: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    chartOptions: {
      legend: {
        display: false,
      },
      responsive: false,
    },
  }),
  computed: {
  },
  watch: {
  },
  created() {
  },
  methods: {
    setColor() {
      this.$root.$emit('colors');
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
  },
};
</script>
