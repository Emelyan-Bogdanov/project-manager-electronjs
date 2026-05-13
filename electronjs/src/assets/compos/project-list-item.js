Vue.component("project-list-item", {
  name: "project-list-item",
  props: {
    projectId: { default: null },
    name: { type: String, default: "Projet" },
    members: { default: 0 },
    tasks: { default: 0 },
    status: { type: String, default: "En cours" },
    statusClass: { type: String, default: "status-progress" },
    color: { type: String, default: "#ff9838" },
  },
  methods: {
    onClick() {
      this.$emit("select", this.projectId);
    },
  },
  template: `
    <div class="project-item" @click="onClick" style="cursor: pointer;">
      <div class="project-item-left">
        <div class="project-dot" :style="{ background: color }"></div>
        <div>
          <div class="project-item-name">{{ name }}</div>
          <div class="project-item-meta">{{ members }} membres &middot; {{ tasks }} t\u00e2ches</div>
        </div>
      </div>
      <div class="project-item-status" :class="statusClass">{{ status }}</div>
    </div>`,
});
