<template>
  <div id="corpus-topic">
    <h2>Topics</h2>
    <b-row>
      <b-col
        v-for="(t, i) in topic.topics"
        :key="i"
        :cols="2"
        class="my-2"
      >
        <b-card
          :header="`Topic ${i+1}`">
          <span v-html="_.join(t, '<br>')"/>
        </b-card>
      </b-col>
    </b-row>
    <br>
    <b-table
      :fields="fields"
      :items="items"
      small
      hover>
      <template
        slot="text_topic_per_label"
        slot-scope="data">
        <span
          v-if="false"
          v-html="data.value"/>
        <bar-chart
          :chart-data="data.item.chart"
          :options="inlineChartOptions"
          :height="150"/>
      </template>
    </b-table>
  </div>
</template>

<script>
import BarChart from '@/components/Snippets/BarChart';

const _ = require('lodash');

export default {
  components: { BarChart },
  props: {
    topic: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    fields: [
      { key: 'topic_no', label: 'Topic number' },
      { key: 'topic_words', label: 'Topic words' },
      { key: 'text_per_topic', label: 'Number of texts' },
      { key: 'text_topic_per_label', label: 'Number of texts per label' },
    ],
    inlineChartOptions: {
      legend: {
        display: false,
      },
      scales: {
        yAxes: [
          {
            ticks: {
              min: 0,
            },
          },
        ],
      },
    },
  }),
  computed: {
    items() {
      return _.chain(this.topic.topics)
        .map((words, i) => {
          const topic = {};

          _.chain(this.topic.text_topic_per_label[i])
            .each((topicLabel) => {
              _.chain(topicLabel)
                .each((counts, label) => {
                  if (_.isObject(counts)) {
                    _.chain(counts)
                      .each((count, value) => {
                        topic[`${label}: ${value}`] = count;
                      })
                      .value();
                  } else {
                    topic[label] = counts;
                  }
                })
                .value();
            })
            .value();

          return {
            topic_no: i + 1,
            topic_words: words.join(', '),
            text_per_topic: this.topic.text_per_topic[i],
            text_topic_per_label: _.chain(topic)
              .map((v, k) => `${k}: ${v}`)
              .value()
              .join('<br>'),
            chart: {
              labels: _.keys(topic),
              datasets: [
                {
                  data: _.values(topic),
                  backgroundColor: this.colorArrayRandom(_.keys(topic)),
                },
              ],
            },
          };
        })
        .value();
    },
  },
};
</script>
