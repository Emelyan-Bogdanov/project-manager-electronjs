  Vue.component("column-title", {
  name: "column-title",
  props: {
    text : {
        typee:String ,
        default:"Default value"
    },
    count :{
        default:99
    }
  },
  data: function () {
    return {
      // You can remove 'author', 'title', 'description', 'image' here if you handle defaults via props
    };
  },
  methods: {},
  template: `
    <div class="column-title">
{{text}} <span class="text-secondary fs-5">({{count}})</span>
    </div>
`,
});
