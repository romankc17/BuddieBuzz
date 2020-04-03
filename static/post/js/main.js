<script type="text/javascript">
      $(document).ready(function(event){
      {% for post in posts %}
        $(document).on('click', '#like_button{{ post.id }}', function(event){
          event.preventDefault();
          var post_id=$(this).attr('value');
          $.ajax({
            type:'POST',
            url : '{% url "post_like" %}',
            data:{'post_id':post_id, 'csrfmiddlewaretoken':'{{ csrf_token }}' },
            dataType: 'json',
            success: function(data){
                if (data.is_liked){
                    document.getElementById("like_button{{post.id}}").innerHTML = `Unlike(${data.countLike})`;
                }
                else{
                    document.getElementById("like_button{{post.id}}").innerHTML = `Like(${data.countLike})`;
                }
            },
            });
         });
         {% endfor %}
        });
    </script>