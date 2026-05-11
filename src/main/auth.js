/*
* verify if logged in
* store infos
*/

const Store = require("electron-store")

const store = new Store()

function isLoggedIn(){
    const user = user.get("user");

    const userId = user.UserId;
    // verift user credentiels
    return true
}

function saveLogin(userid){
    store.set("user",{
        UserId:userid
    })
}

module.exports = {
    saveLogin , 
    isLoggedIn
}