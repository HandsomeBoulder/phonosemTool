<template>
  <q-layout view="lHh Lpr lFf">
    <!-- header -->
    <q-header elevated>
      <q-toolbar>
        <q-btn flat round dense icon="menu" class="q-mr-sm" />
        <q-avatar>
          <img src="src\assets\book.svg" style="width:48px; height:auto">
        </q-avatar>

        <q-toolbar-title>phonosemTool</q-toolbar-title>

      </q-toolbar>
    </q-header>
    <!-- page -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
</script>
