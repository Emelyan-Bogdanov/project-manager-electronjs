Vue.component("tag-compo", {
  name: "tag-compo",
  props: {
    checked: {
      type: Boolean,
      default: false,
    },
    count: {
      default: 0,
    },
    label: {
      type: String,
      default: "Tag",
    },
  },
  data: function () {
    return {};
  },
  methods: {
    clicked: function () {
      this.$emit("toggle", this.label);
    },
  },
  template: `<div class="tag" @click="clicked">
                <input class="form-check-input" type="checkbox" :checked="checked" @click.stop />
                <span class="tag-name">{{label}}</span>
                <span class="count">{{count}}</span>
          </div>`,
});
