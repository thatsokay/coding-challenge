let app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data,
    methods: {
        handleSubmit: function() {
            if (!this.url) {
                return
            }
            if (!this.url.includes('://')) {
                this.url = 'http://' + this.url
            }
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
            fetch(`/api/get_jobs?limit=${this.limit}&offset=${(this.page - 1) * this.limit}`)
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
            })
            .then(json => {
                this.jobs = json
            })
        },
        nextPage: function() {
            fetch(`/api/get_jobs?limit=${this.limit}&offset=${(this.page) * this.limit}`)
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
            })
            .then(json => {
                if (json.length) {
                    this.page += 1
                    this.jobs = json
                }
            })
        },
        prevPage: function() {
            if (this.page > 1) {
                this.page -= 1
                this.updateJobs()
            }
        },
    },
    mounted: function() {
        setInterval(this.updateJobs, 5000)
    },
})
