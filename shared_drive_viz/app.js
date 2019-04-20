Vue.component('directory-accordion', {
    data: function () {
        return {
        count: 0
        }
    },
    props: ['folders', 'offset'],
    template: `
    <div v-bind:style="{'padding-left': offset + 'px'}">
    <ul uk-accordion="multiple: true">
    <li v-for="folder in Object.keys(folders)">
    <a class="uk-accordion-title" href="#">{{folder}}</a>
    <div class="uk-accordion-content">
    <template v-if="Object.keys(folders[folder]).length != 0">
    <directory-accordion :folders="folders[folder]" :offset="offset + 20"></directory-accordion>
    </template>
    <template v-else>
    <p>empty</p>
    </template>
    </div>
    </li>
    </ul>
    </div>
    `
})

var app = new Vue({
    el: '#app',
    data: {
        directory_data: {}
    }
})

app.directory_data = data;
