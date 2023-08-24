package net.legacyfabric.multifilament.task;

import java.io.File;
import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;

import javax.inject.Inject;

import org.gradle.api.file.DirectoryProperty;
import org.gradle.api.provider.Property;
import org.gradle.api.tasks.Input;
import org.gradle.api.tasks.InputDirectory;

import net.fabricmc.mappingio.MappingReader;
import net.fabricmc.mappingio.MappingWriter;
import net.fabricmc.mappingio.format.MappingFormat;
import net.fabricmc.mappingio.tree.MemoryMappingTree;
import net.fabricmc.mappingio.tree.VisitOrder;

public abstract class UnifyMappingsTask extends MappingOutputTask {
	@Inject
	public UnifyMappingsTask() {
		this.getOutputFormat().convention(MappingFormat.ENIGMA);
	}

	@Input
	public abstract Property<String> getUnifiedDir();

	@InputDirectory
	public abstract DirectoryProperty getVersionedDir();

	void pre() throws IOException {
		File file = new File(this.getVersionedDir().getAsFile().get().getParentFile(), this.getUnifiedDir().get());
		file.delete();
		Files.move(this.getOutputDir().getAsFile().get().toPath(), file.toPath());
	}

	void run(MappingWriter var1) throws IOException {
		File file = new File(this.getVersionedDir().getAsFile().get().getParentFile(), this.getUnifiedDir().get());
		MemoryMappingTree treeView = new MemoryMappingTree();
		MappingReader.read(file.toPath(), treeView);
		MemoryMappingTree mappingTree = new MemoryMappingTree();
		MappingReader.read(this.getVersionedDir().getAsFile().get().toPath(), mappingTree);
		mappingTree.accept(treeView);
		treeView.accept(var1, VisitOrder.createByName());

		Files.walkFileTree(file.toPath(), new FileVisitor<Path>() {
			@Override
			public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
				file.toFile().delete();
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFileFailed(Path file, IOException exc) throws IOException {
				return FileVisitResult.TERMINATE;
			}

			@Override
			public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
				dir.toFile().delete();
				return FileVisitResult.CONTINUE;
			}
		});

		Files.walkFileTree(this.getVersionedDir().getAsFile().get().toPath(), new FileVisitor<Path>() {
			@Override
			public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
				file.toFile().delete();
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFileFailed(Path file, IOException exc) throws IOException {
				return FileVisitResult.TERMINATE;
			}

			@Override
			public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
				dir.toFile().delete();
				return FileVisitResult.CONTINUE;
			}
		});
	}
}
