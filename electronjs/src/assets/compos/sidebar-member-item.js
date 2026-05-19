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
    },
    userId: {
      type: [Number, String],
      default: null
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
    goToProfile() {
      if (this.userId) {
        window.electronAPI.navigate("profile.html?user=" + this.userId);
      }
    },
  },
  template: `
    <div class="member-item clicked" @click="goToProfile">
        <img v-if="url" :src='url' alt="" />
        <div v-else class="member-avatar-placeholder">{{ initials(name) }}</div>
        <div>
            <div class="member-name">{{name}}</div>
            <div class="member-time">{{time}}</div>
        </div>
    </div>
    `,
});
