let app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data,
    methods: {
        handleSubmit: function() {
            fetch('/api/add_job', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({url: this.url}),
            })
            this.url = ''
        },
        updateJobs: function() {
            fetch(`/api/get_jobs?limit=${this.limit}&offset=${this.page * this.limit}`)
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
            })
            .then(json => {
                this.jobs = json
            })
        },
    },
    mounted: function() {
        setInterval(this.updateJobs, 5000)
    },
})
