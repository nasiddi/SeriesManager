<template>
  <div>
    <b-form @submit="onSubmit">
      <b-row class="mt-5">
        <b-col>
          <b-form-group
            label-for="name"
          >
            <b-form-input
              id="name"
              v-model="form.name"
              type="text"
              placeholder="Username"
              required
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group
            label-for="password"
          >
            <b-form-input
              id="password"
              v-model="form.password"
              type="password"
              required
              placeholder="Password"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-button
            type="submit"
            variant="primary"
            block
          >Login</b-button>
        </b-col>
      </b-row>

      <b-alert
        :show="showAlerts.success"
        variant="success"
      >
        Login successful
      </b-alert>
      <b-alert
        :show="showAlerts.error"
        variant="danger"
      >
        Login failed
      </b-alert>

    </b-form>
  </div>
</template>

<script>
const _ = require('lodash');

export default {
  data: () => ({
    form: {
      name: '',
      password: '',
    },
    showAlerts: {
      success: false,
      error: false,
    },
  }),
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.showAlerts = _.mapValues(this.showAlerts, () => false);
      this.$auth.login(
        {
          name: this.form.name,
          password: this.form.password,
        },
        () => {
          this.showAlerts.error = true;
        },
      );
    },
  },
  metaInfo: {
    title: 'Login',
  },
};
</script>
