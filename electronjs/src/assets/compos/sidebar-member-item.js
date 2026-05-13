// create the component
Vue.component("sidebar-member-item", {
  name: "sidebar-member-item",
  props: {
    url : {
        type:String ,
        default: "https://i.pravatar.cc/100?img=1"
    },
    name:{
        type:String ,
        default:"Default value"
    },
    time : {
      type:String,
      default:"[default value]" // hour:minute +  "for this week" , example : 08:06
    }
  },
  data: function () {
    // unlike app , the compo's data has to be a function
    return {};
  },
  methods: {},
  template: `
    <div class="member-item">
        <img :src='url' alt="" />
        <div>
            <div class="member-name">{{name}}</div>
            <div class="member-time">{{time}}</div>
        </div>
    </div>
    `,
});
