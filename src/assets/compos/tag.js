// create the component
Vue.component("tag-compo", {
  name: "tag-compo",
  props: ["label","count"], // html tags like : <post-compo author="ibrahim"></post-compo>
  data: function () {
    // unlike app , the compo's data has to be a function
    return {
      checked:false
    };
  },
  methods: {
    check: function () {
      this.checked = !this.checked;
    },
  },
  template: `<div class="tag">
                <input class="form-check-input" type="checkbox"/>
                <span class="tag-name">{{label}}</span>
                <span class="count">{{count}}</span>
          </div>`
});