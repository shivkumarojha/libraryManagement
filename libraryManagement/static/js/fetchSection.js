let sectionId = document.getElementById('id_section').innerHTML = '-----'
let url = "{% url 'library:fetchSection' %}"
    async function fetchSection(e){
        let id = e.target.value
        let response = await fetch("{% url 'library:fetchSection' %}", {
            method: 'get',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'ContentType': 'application/json',
                'classId': id
            }
        })

        //let data = await response.json()
        let data = await response.text()
        console.log(await data)
        sectionId = document.getElementById('id_section').innerHTML = data
    }