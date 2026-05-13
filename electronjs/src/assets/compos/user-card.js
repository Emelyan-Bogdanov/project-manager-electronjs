// create the component
Vue.component("user-card-item", {
  name: "user-card-item",
  props: {
    profile: {
      type: String,
      default: "https://randomuser.me/api/portraits/men/75.jpg",
    },
    username: {
      type: String,
      default: "DEFAULT",
    },
    location: {
      type: String,
      default: "DEFAULT LOCATION",
    },
    tags: {
      type: Array,
      default: () => ["tag1", "tag2", "tag1"],
    },
  },

  data: function () {
    // unlike app , the compo's data has to be a function
    return {};
  },
  methods: {},
  template: `
    <div class="col-lg-4 col-md-6 user-item">
            <div class="user-card">
            <div class="user-top">
                <img
                :src="profile"
                class="user-img"
            />

            <div>
              <div class="user-name">
                <p>{{username}}</p>
              </div>
              <div class="user-location">{{location}}</div>
            </div>
            </div>

            <div class="tags">
                <span class="tag" v-for="tag in tags">{{tag}}</span>
            </div>
          </div>
      </div>`,
});
