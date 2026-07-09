import {createStore} from 'vuex';
import router from '../router/index.js';
const store = createStore(
    {
        state: {
            user:{
                token: null,
                roles : [],
                active: false
            }
        },
        mutations: {
            setUser(state, value){
                localStorage.setItem("user",JSON.stringify(value));
                state.user = value;
            },
            logout(state){
                localStorage.removeItem("user");
                state.user = {
                    token: null,
                    roles : [],
                    active: false
                }
            }
        },
        getters:{
            getToken(state){
                return state.user.token;
            },
            getUser(state){
                return state.user; 
            },
            getRoles(state){
                return state.user.roles;
            },
            getActive(state){
                return state.user.active;
            }
        },
        actions:{
            fetchUser({commit}){
                fetch(import.meta.env.VITE_SERVER+"/fetchUser",{
                    method:"GET",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token": this.getters.getToken
                    }
                }).then(r=>{
                    if(r.status==200){
                        r.json().then(data=>{
                            commit("setUser",data);
                        })
                    }
                    else if(r.status==401 || r.status==403){
                        router.push({name:"login"});
                        commit("logout");
                    }
                }
                )
            }
        }
    }
)

export default store;