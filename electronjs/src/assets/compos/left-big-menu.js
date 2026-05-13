// create the component
Vue.component("left-big-menu", {
  name: "left-big-menu",
  props: {
    compName:{
        type:String,
        default:"vecteurs"
    }
  },

  data: function () {
    // unlike app , the compo's data has to be a function
    return {};
  },
  methods: {},
  template: `
    
    <div>
          <!-- logo pour la socièté -->
          <company-logo :compName="compName"></company-logo>

          <!-- MENU -->
          <div class="sidebar-title">Menu</div>

          <side-menu-button
            biclass="bi-house-fill"
            count="13"
            span-text="kkkkkkkkkk"
          >
          </side-menu-button>

          <side-menu-button biclass="bi-check2-square"> </side-menu-button>

          <side-menu-button 
            biclass="bi-check2-square" 
            span-text="Tâches"
            url="tasks.html">
          </side-menu-button>

          <side-menu-button biclass="bi-chat-dots" span-text="Tasks">
          </side-menu-button>

          <!-- PROJECTS -->

          <sidebar-section-header :has-plus="false"></sidebar-section-header>

          <div class="tools">
            <side-menu-button
              biclass="bi-stack"
              span-text="Publications"
            ></side-menu-button>
            
            <side-menu-button
              biclass="bi-files"
              span-text="Fichiers"
            ></side-menu-button>

            <side-menu-button
              biclass="bi-people"
              span-text="Utilisateurs"
              url="allUsers.html"
            ></side-menu-button>
          </div>

          <!-- MEMBERS -->
          <sidebar-section-header title="Membres de projet">
          </sidebar-section-header>

          <div class="members">
            <sidebar-member-item></sidebar-member-item>
            <sidebar-member-item></sidebar-member-item>
            <sidebar-member-item></sidebar-member-item>
            <sidebar-member-item></sidebar-member-item>
            <sidebar-member-item></sidebar-member-item>
            <sidebar-member-item></sidebar-member-item>
            <sidebar-member-item></sidebar-member-item>
            <sidebar-member-item></sidebar-member-item>
          </div>
        </div>`,
});
