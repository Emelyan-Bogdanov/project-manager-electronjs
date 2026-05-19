Vue.component("sidebar-member-item", {
  name: "sidebar-member-item",
  props: {
    url : {
        type:String ,
        default: ""
    },
    name:{
        type:String ,
        default:"Default value"
    },
    time : {
      type:String,
      default:"[default value]"
    }
  },
  data: function () {
    return {};
  },
  methods: {
    getAvatarSrc(u) {
      return u || "../assets/imgs/default-profile.svg";
    },
    initials(n) {
      return (n || "U").split(" ").filter(Boolean).slice(0, 2).map(p => p[0].toUpperCase()).join("");
    },
  },
  template: `
    <div class="member-item">
        <img v-if="url" :src='url' alt="" />
        <div v-else class="member-avatar-placeholder">{{ initials(name) }}</div>
        <div>
            <div class="member-name">{{name}}</div>
            <div class="member-time">{{time}}</div>
        </div>
    </div>
    `,
});
