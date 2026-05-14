Vue.component("left-big-menu", {
  name: "left-big-menu",
  props: {
    compName: {
      type: String,
      default: "Vecteurs",
    },
  },
  data: function () {
    return {
      members: [],
    };
  },
  async mounted() {
    try {
      const users = await window.electronAPI.getUsers();
      this.members = users.map(u => ({
        id: u.id,
        name: u.name || u.username,
        url: u.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(u.name || u.username)}&background=f97316&color=fff`,
      }));
    } catch (e) {
      console.error("Error loading sidebar members:", e);
    }
  },
  methods: {
    logout: function () {
      if (window.electronAPI && window.electronAPI.logout) {
        window.electronAPI.logout().then(() => {
          window.electronAPI.navigate("src/templates/auth/login.html");
        });
      }
    },
  },
  template: `
    <div>
      <company-logo :compName="compName"></company-logo>

      <div class="sidebar-title">Menu</div>

      <side-menu-button
        biclass="bi-house-fill"
        count="0"
        span-text="Tableau de bord"
        url="dashboard.html"
      ></side-menu-button>

      <side-menu-button
        biclass="bi-check2-square"
        span-text="Tâches"
        url="tasks.html"
      ></side-menu-button>

      <sidebar-section-header :has-plus="false"></sidebar-section-header>

      <div class="tools">
        <side-menu-button
          biclass="bi-stack"
          span-text="Projets"
          url="projects.html"
        ></side-menu-button>

        <side-menu-button
          biclass="bi-files"
          span-text="Fichiers"
          url="files.html"
        ></side-menu-button>

        <side-menu-button
          biclass="bi-people"
          span-text="Utilisateurs"
          url="allUsers.html"
        ></side-menu-button>

        <side-menu-button
          biclass="bi-person"
          span-text="Profil"
          url="profile.html"
        ></side-menu-button>
      </div>

      <sidebar-section-header title="Membres de projet"></sidebar-section-header>

      <div class="members">
        <sidebar-member-item
          v-for="m in members"
          :key="m.id"
          :url="m.url"
          :name="m.name"
        ></sidebar-member-item>
      </div>

      <div class="sidebar-logout" style="margin-top: auto; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.08);">
        <a href="#" class="menu-link" @click.prevent="logout">
          <div class="menu-left">
            <i class="bi bi-box-arrow-left"></i>
            <span>Déconnexion</span>
          </div>
        </a>
      </div>
    </div>`,
});
