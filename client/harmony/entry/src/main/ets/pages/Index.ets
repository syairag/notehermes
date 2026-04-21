// Index.ets - Main Home Page
@Entry
@Component
struct Index {
  @State message: string = 'NoteHermes';

  build() {
    Row() {
      Column() {
        Text(this.message)
          .fontSize(32)
          .fontWeight(FontWeight.Bold)
      }
      .width('100%')
    }
    .height('100%')
  }
}
