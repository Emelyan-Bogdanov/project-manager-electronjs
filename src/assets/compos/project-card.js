Vue.component("project-card", {
  name: "project-card",
  props: {
    tags: {
      type: Array,
      default: () => ["tag1", "tag2", "tag3"],
    },
    title: {
      type: String,
      default: "This is a title by default",
    },
    description: {
      type: String,
      default:
        "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Earum, aspernatur. Aliquid deleniti impedit, quisquam, velit ad utreiciendis provident voluptatem sapiente optio recusandae, est necessitatibus autem dolores quos quibusdam? Amet!",
    },
    author: {
      type: String,
      default: "unknown",
    },
    image: {
      type: String,
      default: "../assets/imgs/projet-default.png",
    },
    views: {
      default: 99,
    },
    commentsCount: {
      default: 99,
    },
    deadline: {
      type: String,
      default: "12 Feb",
    },
  },
  data: function () {
    return {
      // You can remove 'author', 'title', 'description', 'image' here if you handle defaults via props
    };
  },
  methods: {},
  template: `
        <div class="task-card">
              <div class="tags">
                <span class="tag tag-orange" v-for="tag in tags">{{tag}}</span>
              </div>

              <div class="task-title">{{title}}</div>

              <div class="task-text">
                {{description}}
              </div>

              <div class="date-box">
                <i class="bi bi-calendar3"></i>
                {{deadline}}
              </div>

              <div class="card-footer-custom">
                <div class="avatars">
                <!-- to modify later -->
                  <img src="https://i.pravatar.cc/100?img=4" />
                  <img src="https://i.pravatar.cc/100?img=4" />
                  <img src="https://i.pravatar.cc/100?img=4" />
                </div>

                <div class="text-secondary small">
                  <i class="bi bi-chat"></i> {{commentsCount}}
                </div>
              </div>
            </div>
`,
});
