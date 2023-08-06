

This is an implementation of [Context Programming](https://github.com/nanw1103/context-programming), for CLI program.

It has the following configuration data structure, to support multiple CLIs, and multiple profiles per CLI.

```
<repo-path>
    <cli-name-1>
        profile
            default
            <profile-name-11>.yml
            <profile-name-12>.yml
            ...
        context
            <profile-name-11>
                <application-specific-data-111>.yml
                <application-specific-data-112>.yml
                ...
            <profile-name-12>
                <application-specific-data-121>.yml
                <application-specific-data-122>.yml
                ...
            ...
    <cli-name-2>
        profile
            default
            <profile-name-21>.yml
            <profile-name-22>.yml
            ...
        context
            <profile-name-21>
                <application-specific-data-211>.yml
                <application-specific-data-212>.yml
                ...
            <profile-name-22>
                <application-specific-data-221>.yml
                <application-specific-data-222>.yml
                ...
            ...
    ...
```

The efault repo-path is: <user-home-dir>/<cli-name>
Take two different CLI programs _helloctl_ and _kittyctl_ as examples. Each of them may have multiple environments. By default the structure will be:

```
~
    helloctl
        profile
            default
            my-hello-env1.yml
            my-hello-env2.yml
        context
            my-hello-env1
                my-data1.yml
                my-data2.yml
            my-hello-env2
                my-data1.yml
    kittyctl
        profile
            default
            my-kitty-env.yml
        context
            my-kitty-env
                my-data1.yml
```

