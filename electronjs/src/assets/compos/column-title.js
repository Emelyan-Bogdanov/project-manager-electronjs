Vue.component("column-title", {
  name: "column-title",
  props: {
    text: {
      type: String,
      default: "Default value",
    },
    count: {
      default: 0,
    },
  },
  template: `
    <div class="column-title">
{{text}} <span class="text-secondary fs-5">({{count}})</span>
    </div>
`,
});
