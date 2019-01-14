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
          <span>Premiere </span><span class="mt-2"><strong>{{ show.premiere }}</strong></span>
        </b-col>
        <b-col class="text-center mt-2">
          <span>Final </span><span class="mt-2"><strong>{{ show.final }}</strong></span>
        </b-col>
        <b-col class="text-center mt-2">
          <span class="mt-2"><b>{{ show.genre1 }} </b></span><span>{{ show.genre2 }}</span>
        </b-col>
      </b-row>
      <hr>
      <b-row>
        <b-col class="text-center mt-2">
          <span>Seasons </span><span class="mt-2"><strong>{{ show.seasons }}</strong></span>
        </b-col>
        <b-col class="text-center mt-2">
          <span>Episodes </span><span class="mt-2"><strong>{{ show.episodes }}</strong></span>
        </b-col>
        <b-col class="text-center mt-2">
          <span>Hours </span><span class="mt-2"><strong>{{ show.duration }}</strong></span>
        </b-col>
        <b-col class="text-center mt-2">
          <span>GB </span><span class="mt-2"><strong>{{ show.size }}</strong></span>
        </b-col>
      </b-row>
      <hr>
      <b-row
        lg
        class="mt-3">
        <b-col class="text-center mt-2">
          <span>Minutes per Episode </span><span class="mt-2"><b>{{ show.avg_duration }}</b></span>
        </b-col>
        <b-col class="text-center mt-2">
          <span>MB per Episode </span><span class="mt-2"><b>{{ show.avg_size }}</b></span>
        </b-col>
        <b-col class="text-center mt-2">
          <span>Episodes per Season </span><span class="mt-2"><b>{{ show.avg_e_per_s }}</b></span>
        </b-col>
      </b-row>
      <hr>
      <b-row lg>
        <b-col class="text-center">
          <div
            v-for="(k, v) in sortByCount(show.extension)"
            :key="v">
            <span class="mt-2">
            <strong>{{ v }}</strong> {{ k }}</span><br>
          </div>
        </b-col>
        <b-col class="text-center">
          <div
            v-for="(k, v) in sortByCount(show.quality)"
            :key="v">
            <span class="mt-2">
            <strong>{{ v }}</strong> {{ k }}</span><br>
          </div>
        </b-col>
        <b-col class="text-center">
          <div
            v-for="(k, v) in sortByCount(show.ratio)"
            :key="v">
            <span class="mt-2">
            <strong>{{ v }}</strong> {{ k }}</span><br>
          </div>
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
      this.$snotify.error(_.values(this.show.extension), { timeout: 0 });
    },
    sortByCount(data) {
      const d = _.chain(data)
        .map((val, key) => ({ name: key, count: val }))
        .sortBy('count')
        .reverse()
        .keyBy('name')
        .mapValues('count')
        .value();
      return d;
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
