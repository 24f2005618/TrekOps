import {createStore} from 'vuex';

const store = createStore(
    {
        state: {
            user:{
                token: null,
                roles : []
            }
        },
        mutations: {
            setUser(state, value){
                localStorage.setItem("user",JSON.stringify(value));
                state.user = value;
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
            }
        }
    }
)

export default store;