# Generated by Django 2.2 on 2020-04-06 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment", options={"verbose_name": "评论", "verbose_name_plural": "评论"},
        ),
        migrations.AlterModelOptions(
            name="post",
            options={
                "ordering": ["-id"],
                "verbose_name": "文章",
                "verbose_name_plural": "文章",
            },
        ),
        migrations.AddField(
            model_name="post", name="pv", field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="post", name="uv", field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="category",
            name="status",
            field=models.PositiveIntegerField(
                choices=[(0, "删除"), (1, "正常")], default=1, verbose_name="状态"
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="status",
            field=models.PositiveIntegerField(
                choices=[(0, "删除"), (1, "正常")], default=1, verbose_name="状态"
            ),
        ),
        migrations.AlterField(
            model_name="link",
            name="status",
            field=models.PositiveIntegerField(
                choices=[(0, "删除"), (1, "正常")], default=1, verbose_name="状态"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.PositiveIntegerField(
                choices=[(0, "删除"), (1, "正常"), (2, "草稿")], default=1, verbose_name="状态"
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="status",
            field=models.PositiveIntegerField(
                choices=[(0, "删除"), (1, "正常")], default=1, verbose_name="状态"
            ),
        ),
    ]
